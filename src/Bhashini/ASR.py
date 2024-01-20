from src.Bhashini.bhashini_config import *
import requests
import json

class ASR:
    def __init__(self) -> None:
        pass
    
    def from_base64(self,base_64_encoding,language):
        payload=Payloads().ASRPayload(Languages[language],base_64_encoding,ASRServiceIDs[language])
        header=Payloads().InferenceAPIHeader()
        x=json.dumps(payload)
        response=requests.post(url="https://dhruva-api.bhashini.gov.in/services/inference/pipeline",data=x,headers=header)
        if response.status_code==200:
            response=response.json()
            return response
        