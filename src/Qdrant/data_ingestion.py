from datasets import load_dataset
from dataclasses import dataclass
import os
from src.logger import logging

@dataclass
class DataIngestorConfig:
    dataset_path=os.path.join("data","data.csv")

class DataIngestor:
    def __init__(self) -> None:
        self.file_path=DataIngestorConfig().dataset_path
    
    def initialize_data_ingestion(self,dataset_name:str)->None:
        try:
            logging.info("data ingestion started")
            data=load_dataset(dataset_name)
            dataset=data['train'].data
            df=dataset.to_pandas()
            df.to_csv(self.file_path)
            logging.info("data ingested successfully")
            return self.file_path
        except Exception as e:
            logging.info(f"some error occured {e}")
            raise ConnectionError("connection error")