import requests
from dotenv import load_dotenv
import os
import json
from src.logger import logging
load_dotenv()

BHASINI_USERID=os.getenv("BHASINI_USERID")
BHASINI_API_KEY=os.getenv("BHASINI_API_KEY")

PiplineSearchEndPoint="https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
InferenceApiEndPoint="https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

Languages={
    "english":"en",
    "hindi":"hi",
    "bengali":'bn',
    "kannada":'kn',
    "malyalam":'ml',
    "marathi":'mr',
    "oriya":'or',
    "tamil":'ta',
    "telugu":'te',
    "punjabi":'pa',
    "gujrati":'gu'
}
ASRServiceIDs={
   "bengali":"ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
   "english":"ai4bharat/whisper-medium-en--gpu--t4",
   "gujrati":"ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
   "hindi":"ai4bharat/conformer-hi-gpu--t4",
   "kannada":"ai4bharat/conformer-multilingual-dravidian-gpu--t4",
    "malyalam":"ai4bharat/conformer-multilingual-dravidian-gpu--t4",
   "marathi":"ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
    "oriya":"ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
   "punjabi":"ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
    "tamil":"ai4bharat/conformer-multilingual-dravidian-gpu--t4",
    "telugu":"ai4bharat/conformer-multilingual-dravidian-gpu--t4"}

TTSServiceIDs={
    "bengali":"ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
    "english":"ai4bharat/indic-tts-coqui-misc-gpu--t4",
    "gujrati":"ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
    "hindi":"ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
    "kannada":"ai4bharat/indic-tts-coqui-dravidian-gpu--t4",
    "malyalam":"ai4bharat/indic-tts-coqui-dravidian-gpu--t4",
    "marathi":"ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
    "oriya":"ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
    "punjabi":"ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
     "tamil":"ai4bharat/indic-tts-coqui-dravidian-gpu--t4",
   "telugu":"ai4bharat/indic-tts-coqui-dravidian-gpu--t4"}

TraslationServiceIDs={
   "serviceID":"ai4bharat/indictrans-v2-all-gpu--t4"} # single service id  is there for all type of translation

PipeLineIDs={
    "Meity":"64392f96daac500b55c543cd",
    "AI4Bharat":"643930aa521a4b1ba0f4c41d"
}

PipeLineTasks={
    "automatic_speech_recoginition":'asr',
    "translation":'translation',
    "text_to_speech":'tts'
    }


class Payloads:
    def __init__(self) -> None:
        pass
    def ASRPayload(self,language,audio_encoding:str,serviceId,audio_format='wav'):
        """we 11 languages decribed in the above enum class
        and audio encoding should be in base64 of mp3 or wav format"""
        payload={
                    "pipelineTasks": [
                        {
                            "taskType": "asr",
                            "config": {
                                "language": {
                                    "sourceLanguage":language
                                },
                                "serviceId":serviceId,
                                "audioFormat": audio_format,
                                "samplingRate": 16000
                            }
                        }
                    ],
                    "inputData": {
                        "input": [
                            {
                                "source": "null"
                            }
                        ],
                        "audio": [
                            {
                                "audioContent":audio_encoding
                            }
                        ]
                    }
                }
        return payload

    def TTSPayload(self,language,serviceId,content:str,gender:str='female'):
        payload={
                    "pipelineTasks": [       
                        {
                            "taskType": "tts",
                            "config": {
                                "language": {
                                    "sourceLanguage": language
                                },
                                "serviceId": serviceId,
                                "gender": gender
                            }
                        }
                    ],
                    "inputData": {
                        "input": [
                            {
                                "source":content
                            }
                        ],
                        "audio": [
                            {
                                "audioContent": None
                            }
                        ]
                    }
                }
        return payload
    
    def TranslationPayload(self,source_lang,target_lang,content:str,serviceId=TraslationServiceIDs['serviceID']):
        payload={
                    "pipelineTasks": [
                        {
                            "taskType": "translation",
                            "config": {
                                "language": {
                                    "sourceLanguage": source_lang,
                                    "targetLanguage": target_lang
                                },
                                "serviceId":serviceId
                            }
                        }
                    ],
                    "inputData": {
                        "input": [
                            {
                                "source":content
                            }
                        ],
                        "audio": [
                            {
                                "audioContent": None
                            }
                        ]
                    }
                }
        return payload
    
    def PipeLineSearchPayload(self,task,language,pipelineid):
        payload={
                "pipelineTasks": [
                    {
                        "taskType": task,
                        "config": {
                            "language": {
                                "sourceLanguage":language
                            }
                        }
                    }
                ],
                "pipelineRequestConfig": {
                    "pipelineId": pipelineid
                }
            }
        return payload
    
    def AuthorizationHeader(self):
        header={
            'userID':BHASINI_USERID,
            'ulcaApiKey':BHASINI_API_KEY
        }
        return header
    
    def InferenceAPIHeader(self):
        with open(os.path.join("src","Bhashini","inference_key.json"),'r') as file:
            api_header=file.read()
        header={"Content-Type":"application/json","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Cache-Control":"no-cache"}
        js_data=json.loads(api_header)
        header['Authorization']=js_data['Authorization']
        return header

def update_inference_key():
    try:
        payload=Payloads().PipeLineSearchPayload('asr','hi',PipeLineIDs["Meity"])
        header={"Content-Type":"application/json","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Cache-Control":"no-cache"}
        header['userID']=BHASINI_USERID
        header['ulcaApiKey']=BHASINI_API_KEY
        res=requests.post(url=PiplineSearchEndPoint,data=json.dumps(payload),headers=header)
        if res.status_code==200:
            response=res.json()
            data=response["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]
            name=data['name']
            value=data['value']
            api_key={name:value}
            with open(os.path.join("src","Bhashini","inference_key.json"),'w') as file:
                file.write(json.dumps(api_key))
    except Exception as e:
        logging.info("inference key is not updated")