from datasets import load_dataset
from dataclasses import dataclass
import os

@dataclass
class DataLoaderConfig:
    dataset_path=os.path.join("data","data.csv")

class DataLoader:
    def __init__(self) -> None:
        self.file_path=DataLoaderConfig().dataset_path
    
    def initialize_data_ingestion(self,dataset_name:str)->None:
        try:
            data=load_dataset(dataset_name)
            dataset=data['train'].data
            df=dataset.to_pandas()
            df.to_csv(self.file_path)
            return self.file_path
        except Exception as e:
            raise ConnectionError("connection error")