from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler
from dotenv import load_dotenv
import os
import requests
from src.TEXT import Gemini
from src.Bhashini.ASR import ASR
from src.Bhashini.TTS import TTS
from src.settings import BotSettings,button_handler
import base64
from io import BytesIO
from src.MYSQL.sql_handler import sql

load_dotenv()
bot_username=os.getenv("BOT_USERNAME")
api_key=os.getenv("TELEGRAM_BOT_API_TOKEN")
ffmpeg_endpoint=os.getenv("FFMPEG_ENDPOINT")

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    userid=update.effective_user.id
    sql().start(userid)
    reply_markup = BotSettings().SendLanguages()
    await update.message.reply_text("Please select the language:", reply_markup=reply_markup)
    await update.message.reply_text("Please select the chat mode:", reply_markup=BotSettings().SendChatMode())

async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    help=""""
        this is farmers bot. it can give you contexual answers of your queries related to farming. 
        to start the conversation tap /start . on start you will be asked to select the language and the chat mode
        if you have previously selected these settings please ignore it. there are two chat mode in this bot general and farmers help
        general mode for general question answering and farmers help for farming related issues. 
        for text you can use any language and for voice only 11 languages are supported till now.
    """
    await update.message.reply_text(help)


def handle_response(text:str)->str:
    processed=text.lower()
    llm=Gemini()
    ans=llm.generete_ans(processed)
    return ans

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str=update.message.text
    if message_type=='group':
        if bot_username in text:
            new_text:str=text.replace(bot_username," ").strip()
            response=await handle_response(new_text)
        else:
            return
    else:
        response=handle_response(text)
    await update.message.reply_markdown(response)

async def handle_voice_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message=update.message.voice
    userid=update.effective_user.id
    mode=sql().get_mode(userid)
    lang=sql().get_lang(userid)
    file=await message.get_file()
    file_path=file.file_path
    res=requests.post(ffmpeg_endpoint,{"url":file_path})
    data=res.json()
    asr=ASR()
    data=asr.from_base64(data['base64Wav'],lang)
    text=data['pipelineResponse'][0]['output'][0]['source']
    llm=Gemini()
    ans=llm.generete_ans(text)
    tts=TTS()
    voice_data=tts.convert_text_speech(ans,lang)
    voice=voice_data['pipelineResponse'][0]['audio'][0]['audioContent']
    b_64_decode=base64.b64decode(voice)
    await update.message.reply_voice(voice=BytesIO(b_64_decode))

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):
    userid=update.effective_user.id
    query=update.callback_query
    await query.answer()
    setting,action=query.data.split()
    await button_handler(userid,action,setting)


async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f"error occured {update} {context.error}")

