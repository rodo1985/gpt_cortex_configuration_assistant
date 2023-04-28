import os
import yaml
# from langchain.llms import OpenAI

with open('app_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

OPENAI_API_KEY = config['openai']['api_key']


os.environ["OPENAI_API_KEY"] =  OPENAI_API_KEY 


def main():
    print('hello')
    # llm = OpenAI(temperature=0.9)
    # text = "What would be a good company name for a company that makes colorful socks?"
    # print(llm(text))


if __name__ == '__main__':
    main()
