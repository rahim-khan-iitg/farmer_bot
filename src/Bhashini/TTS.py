from src.Bhashini.bhashini_config import *
import requests
import json
from src.logger import logging
class TTS:
    def __init__(self) -> None:
        pass

    def convert_text_speech(self,message:str,language:str):
        try:
            payload=Payloads().TTSPayload(Languages[language],TTSServiceIDs[language],message,gender='male')
            headers=Payloads().InferenceAPIHeader()
            data=json.dumps(payload)
            inference_api=InferenceApiEndPoint
            res=requests.post(url=inference_api,data=data,headers=headers)
            if res.status_code==200:
                logging.info("TTS done successfully")
                return res.json()
            else:
                return "error"
        except Exception as e:
            logging.info(f"error occured during TTS {e}")

