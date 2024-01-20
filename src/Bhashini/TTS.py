from src.Bhashini.bhashini_config import *
import requests
import json

class TTS:
    def __init__(self) -> None:
        pass

    def convert_text_speech(self,message:str,language:str):
        payload=Payloads().TTSPayload(Languages[language],TTSServiceIDs[language],message,gender='male')
        headers=Payloads().InferenceAPIHeader()
        data=json.dumps(payload)
        inference_api=InferenceApiEndPoint
        res=requests.post(url=inference_api,data=data,headers=headers)
        if res.status_code==200:
            return res.json()
        else:
            return "error"





# if __name__=="__main__":
#     obj=TTS()
#     obj.convert_text_speech("मेरा  नाम रहीम खान है ","hindi")
        