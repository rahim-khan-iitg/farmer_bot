from src.Bhashini.bhashini_config import *
import requests
import json
from src.logger import logging

class ASR:
    def __init__(self) -> None:
        pass
    
    def from_base64(self,base_64_encoding,language):
        try:
            payload=Payloads().ASRPayload(Languages[language],base_64_encoding,ASRServiceIDs[language])
            header=Payloads().InferenceAPIHeader()
            x=json.dumps(payload)
            logging.info("ASR initiated")
            response=requests.post(url="https://dhruva-api.bhashini.gov.in/services/inference/pipeline",data=x,headers=header)
            if response.status_code==200:
                response=response.json()
                logging.info("ASR done successfully")
                return response
        except Exception as e:
            logging.info(f"error occured during ASR {e}")
               