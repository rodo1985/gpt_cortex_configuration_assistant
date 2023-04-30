import os
import yaml
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI

def load_config():
    with open('app_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    OPENAI_API_KEY = config['openai']['api_key']
    os.environ["OPENAI_API_KEY"] =  OPENAI_API_KEY 


def main():

    load_config()

    # with open('docs/App.config.xml') as f:
    #     state_of_the_union = f.read()
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # texts = text_splitter.split_text(state_of_the_union)

    # embeddings = OpenAIEmbeddings()
    # docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])
    # query = "¿Como podria configurar la pelicula del sensor para utilizar 100 imagenes?"
    # docs = docsearch.similarity_search(query)
    
    docs_path = 'docs'
    
    # load all documents in docs folder
    doc_list = os.listdir(docs_path)

    from langchain.document_loaders import TextLoader
    from langchain.indexes import VectorstoreIndexCreator
    
    loaders = []
    for doc_file in doc_list:
        loader = TextLoader(os.path.join(docs_path, doc_file), encoding='utf8')
        loaders.append(loader)

    index = VectorstoreIndexCreator().from_loaders(loaders)

    query = "¿Como agregar mas imagenes a la pelicula del sensor?"
    print(index.query(query))
 
    # template = """Eres un asistente automatico de un software llamado Cortex de la empresa bcnvision. Tu objetivo es poder responder preguntas tecnicas sobre la configuración de este software.
    # Para cualquier pregunta que no sea relacionada con Cortex deberas contestar que no lo sabes o que eres un asistente especializado en Cortex y que no puedes contestar nada que no este relacionado con el software. 
    # Si no sabes responder alguna pregunta indica al usario que se ponga en contacto con el departamente de Backoffice.

    # PREGUNTA: {question}
    # =========
    # {summaries}
    # =========
    # """

    # PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

    # chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)
    
    # query = "¿Como agreagar mas imagenes a la pelicula del sensor?"
    # print(chain({"input_documents": loaders, "question": query}, return_only_outputs=True))

if __name__ == '__main__':
    main()
