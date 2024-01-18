from langchain.vectorstores.qdrant import Qdrant
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

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
        model=GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GEMINI_API_KEY)
        return model
    except Exception as e:
        raise ConnectionError("not connected")



class DataLoader:
    def __init__(self,file_path:str) -> None:
        self.csv_path=file_path

    def initialize_data_loading(self)->None:
        try:
            loader=CSVLoader(self.csv_path,autodetect_encoding=True)
            data=loader.load()
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=4000,chunk_overlap=50)
            docs=text_splitter.split_documents(data)
            embedding_model=load_embedding_model()
            qdrant=Qdrant.from_documents(docs,embedding=embedding_model,url=QDRANT_ENDPOINT,prefer_grpc=True,api_key=QDRANT_API_KEY,collection_name=QDRANT_COLLECTION_NAME)

        except Exception as e:
            raise ConnectionError("connection error")
        

class Qdrant_Retriever:
    def __init__(self) -> None:
        pass

    def connect_to_qdrant_as_retriver(self):
        client=QdrantClient(QDRANT_ENDPOINT,api_key=QDRANT_API_KEY)
        collection_name="big_basket"
        embedding_model=load_embedding_model()
        qdrant=Qdrant(client=client,collection_name=collection_name,embeddings=embedding_model)
        retriver=qdrant.as_retriever()
        return retriver