from src.Bhashini.bhashini_config import *
import requests
from tenacity import retry,stop_after_attempt
from pathlib import Path
from pydub import AudioSegment
from io import BytesIO
import base64

class ASR:
    def __init__(self) -> None:
        pass

    @retry(stop=stop_after_attempt(3))
    def from_base64(self,base_64_encoding:str,language:Languages)->str:
        try:
            payload=Payloads().ASRPayload(Languages['language'].value,base_64_encoding,ASRServiceIDs['language'].value)
            header=Payloads().InferenceAPIHeader()
            response=requests.post(url=InferenceApiEndPoint,data=payload,headers=header)
            if response.status_code==200:
                response=response.json()
                output=response['output']['source']
                return output
        except Exception as e:
            print(f"connection error {e} ")


class AudioConverter:
    def __init__(self) -> None:
        pass

    def convert_ogg_bytes_to_wav(self,ogg_bytes:bytearray)->bytearray:
        ogg_audio = AudioSegment.from_file(BytesIO(ogg_bytes), format="ogg")
        wav_bytes_io = BytesIO()
        ogg_audio.export(wav_bytes_io, format="wav")
        wav_bytes = wav_bytes_io.getvalue()
        return wav_bytes
    def convert_bytes_to_base64(self,audio_bytes:bytearray)->base64.b64encode:
        base64_str=base64.b64encode(audio_bytes)
        return base64_str
    
    def convert_ogg_to_wav_base64(self,ogg_bytes:bytearray)->base64.b64encode:
        wav_bytes=self.convert_ogg_bytes_to_wav(ogg_bytes)
        base64_str=self.convert_bytes_to_base64(wav_bytes)
        return base64_str
    