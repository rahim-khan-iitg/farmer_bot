from src.Bhashini.bhashini_config import *


class TTS:
    def __init__(self) -> None:
        pass

    def convert_text_speech(self,message:str,language:str):
        payload=Payloads().TTSPayload(Languages[language],TTSServiceIDs[language],message)
        headers=Payloads().InferenceAPIHeader()
        inference_api=InferenceApiEndPoint
        