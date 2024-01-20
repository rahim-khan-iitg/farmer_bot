from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from os import getenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

GEMINI_API_KEY=getenv('GEMINI_API_KEY')


class Gemini:
    def __init__(self) -> None:    
        self.template="""your name is  farmers bot. you help farmers by listening their queries and answer them .. Question:{question} 
        let's think step by step ."""
        self.prompt=PromptTemplate.from_template(self.template)
        self.llm=ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=GEMINI_API_KEY)
        self.chain=self.prompt | self.llm

    def generete_ans(self,question:str)->str:
        result=self.chain.invoke({"question":question})
        return result.content
