from src.Qdrant.data_ingestion import DataIngestor
from src.Qdrant.data_loader import DataLoader

if __name__=="__main__":
    dataset_name="shchoi83/agriQA"
    print("data ingestion started")
    data_file_path=DataIngestor().initialize_data_ingestion(dataset_name)
    print("data ingestion completed ")
    print("data loading started")
    DataLoader(data_file_path).initialize_data_loading()
    print("data loading completed")