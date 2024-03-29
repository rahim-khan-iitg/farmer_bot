from langchain.vectorstores.qdrant import Qdrant
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.logger import logging

from qdrant_client import QdrantClient

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
QDRANT_ENDPOINT=os.getenv("QDRANT_ENDPOINT")
QDRANT_COLLECTION_NAME=os.getenv("QDRANT_COLLECTION_NAME")


def load_embedding_model()->None:
    try:
        logging.info("loading google embedding model")
        model=GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GEMINI_API_KEY)
        logging.info("loaded successfully")
        return model
    except Exception as e:
        logging.info(f"error occured during loading the embedding model {e}")
        raise ConnectionError("not connected")



class DataLoader:
    def __init__(self,file_path:str) -> None:
        self.csv_path=file_path

    def initialize_data_loading(self)->None:
        try:
            logging.info("data loading started")
            loader=CSVLoader(self.csv_path,autodetect_encoding=True)
            data=loader.load()
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=4000,chunk_overlap=50)
            docs=text_splitter.split_documents(data)
            embedding_model=load_embedding_model()
            logging.info("loading data to qdrant")
            qdrant=Qdrant.from_documents(docs,embedding=embedding_model,url=QDRANT_ENDPOINT,prefer_grpc=True,api_key=QDRANT_API_KEY,collection_name=QDRANT_COLLECTION_NAME)
            logging.info("data loaded successfully")

        except Exception as e:
            logging.info(f"error occured during data loading {e}")
            raise ConnectionError("connection error")
        

class Qdrant_Retriever:
    def __init__(self) -> None:
        pass

    def connect_to_qdrant_as_retriver(self):
        try:
            logging.info("connecting to qdrant as retriver")
            client=QdrantClient(QDRANT_ENDPOINT,api_key=QDRANT_API_KEY)
            collection_name="agri_qa"
            embedding_model=load_embedding_model()
            qdrant=Qdrant(client=client,collection_name=collection_name,embeddings=embedding_model)
            retriver=qdrant.as_retriever()
            logging.info("retriver connected successfully")
            return retriver
        except Exception as e:
            logging.info(f"error occured during retriver connection {e}")
            raise ConnectionError