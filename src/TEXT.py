from src.Qdrant.data_loader import Qdrant_Retriever
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from os import getenv
import requests
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from src.logger import logging
load_dotenv()

GEMINI_API_KEY=getenv('GEMINI_API_KEY')
MISTRAL_API_KEY=getenv("MISTRAL_API_KEY")
MISTRAL_ENDPOINT=getenv("MISTRAL_ENDPOINT") # this is an openrouter endpoint 

class Gemini:
    def __init__(self) -> None:    
        self.template="""your name is  farmers bot. you help farmers by listening their queries and answer them .. Question:{question} 
        let's think step by step ."""
        self.prompt=PromptTemplate.from_template(self.template)
        self.llm=ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=GEMINI_API_KEY,convert_system_message_to_human=True)
        self.chain=self.prompt | self.llm

    def generete_ans(self,question:str)->str:
        try:
            logging.info("generating ans with gemini")
            result=self.chain.invoke({"question":question})
            logging.info("successfully generated")
            return result.content
        except Exception as e:
            logging.info(f"error occured while generating ans with gemini {e}")
            return "error"
    
    def generate_ans_with_qdrant(self,question:str)->str:
        try:
            retriver1=Qdrant_Retriever().connect_to_qdrant_as_retriver()
            logging.info("connected to qdrant successfully generating ans with gemini")
            qa=RetrievalQA.from_chain_type(llm=self.llm,chain_type='stuff',retriever=retriver1)
            response=qa.invoke(f"""your name is  farmers bot. you help farmers by listening their queries and answer them .. Question:{question} let's think step by step .""")
            logging.info("successfully generated")
            return response['result']
        except Exception as e:
            logging.info(f"error occured {e}")
            return "error"

class Mixtral:
    def __init__(self) -> None:
        self.api_key=MISTRAL_API_KEY
        self.endpoint=MISTRAL_ENDPOINT

    def generete_ans(self,message:str)->dict:
        try:
            prompt=f"""your name is  farmers bot. you help farmers by listening their queries and answer them .. Question:{message} 
            let's think step by step ."""
            json_data={"model": "mistralai/mixtral-8x7b-instruct","messages": [{"role": "user", "content": prompt}]}
            headers={"Authorization":self.api_key,"Content-Type":"application/json","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Connection":"keep-alive"}
            logging.info("generating ans with mistral")
            resp=requests.post(url=self.endpoint,data=json.dumps(json_data),headers=headers)
            resp=resp.json()
            ans=resp['choices'][0]['message']['content']
            logging.info("generated successfully")
            return ans
        except Exception as e:
            logging.info(f"error occured {e}")
            return "error"