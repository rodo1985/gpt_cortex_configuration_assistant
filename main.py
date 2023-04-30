import os
import yaml
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers.regex import RegexParser

def load_config():
    with open('app_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    OPENAI_API_KEY = config['openai']['api_key']
    os.environ["OPENAI_API_KEY"] =  OPENAI_API_KEY 


def main():

    load_config()

    docs_path = 'docs'
    
    # load all documents in docs folder
    doc_list = os.listdir(docs_path)

    texts = None

    for doc_file in doc_list:
        path = os.path.join(docs_path, doc_file)

        with open(path) as f:
            state_of_the_union = f.read()

        # Splitting up the text into smaller chunks for indexing
        text_splitter = CharacterTextSplitter(        
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap  = 200, #striding over the text
            length_function = len,
        )
        if texts is None:
            texts = text_splitter.split_text(state_of_the_union)
        else:
            texts += text_splitter.split_text(state_of_the_union)
        break
    
    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    print(docsearch.embedding_function)

    prompt_template = """Eres un asistente automatico de un software llamado Cortex de la empresa bcnvision. Tu objetivo es poder responder preguntas tecnicas sobre la configuración de este software.
    Para cualquier pregunta que no sea relacionada con Cortex deberas contestar que no lo sabes o que eres un asistente especializado en Cortex y que no puedes contestar nada que no este relacionado con el software. 
    Si no sabes responder alguna pregunta indica al usario que se ponga en contacto con el departamente de Backoffice.

    # Contexto:
    # ---------
    # {context}
    # ---------
    # Pregunta: {question}
    # ---------
    # Respuesta:
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = load_qa_chain(OpenAI(), chain_type="stuff") # we are going to stuff all the docs in at once

    chain.llm_chain.prompt = PROMPT

    # # check the prompt
    # print(chain.llm_chain.prompt.template)

    query = "¿Como puedo configurar el Servidor de deep learning de Cortex? Me podrias dar un ejemplo?"
    docs = docsearch.similarity_search(query)
    print(chain.run(input_documents=docs, question=query))
    
if __name__ == '__main__':
    main()
