from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler
from dotenv import load_dotenv
import os
import requests
from src.TEXT import Gemini,Mixtral
from src.Bhashini.ASR import ASR
from src.Bhashini.TTS import TTS
from src.settings import BotSettings,button_handler
import base64
from io import BytesIO
from src.MYSQL.sql_handler import sql
from src.logger import logging

load_dotenv()
bot_username=os.getenv("BOT_USERNAME")
api_key=os.getenv("TELEGRAM_BOT_API_TOKEN")
ffmpeg_endpoint=os.getenv("FFMPEG_ENDPOINT")
lang='english'

model='gemini'

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    userid=update.effective_user.id
    # sql().start(userid)
    logging.info("start command executed")
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
    logging.info("help command executed")
    await update.message.reply_text(help)


def handle_response(text:str,userid)->str:
    processed=text.lower()
    try:
        # mode=sql().get_mode(userid)
        mode='general'
        if model=='mixtral':
            llm=Mixtral()
            ans=llm.generete_ans(processed)
            logging.info("generated ans using mixtral")
            return ans
        elif model=='gemini' and mode=='fh':
            llm=Gemini()
            ans=llm.generate_ans_with_qdrant(processed)
            logging.info("generated ans using gemini with qdrant")
            return ans
        else:
            llm=Gemini()
            ans=llm.generete_ans(processed)
            logging.info("generated ans using gemini")
            return ans
    except Exception as e:
        logging.info(f"error occured {e}")
        return "having difficulty to connect to LLM"

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        message_type:str=update.message.chat.type
        text:str=update.message.text
        userid=update.effective_user.id
        if message_type=='group':
            if bot_username in text:
                new_text:str=text.replace(bot_username," ").strip()
                response=await handle_response(new_text,userid)
            else:
                return
        else:
            response=handle_response(text,userid)
        await update.message.reply_markdown(response)
    except Exception as e:
        logging.info(f"some error occured {e}")
        await update.message.reply_text("some error occured")

async def handle_voice_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message=update.message.voice
    userid=update.effective_user.id
    # lang=sql().get_lang(userid)
    global lang
    file=await message.get_file()
    file_path=file.file_path
    res=requests.post(ffmpeg_endpoint,{"url":file_path})
    data=res.json()
    asr=ASR()
    data=asr.from_base64(data['base64Wav'],lang)
    text=data['pipelineResponse'][0]['output'][0]['source']
    ans=handle_response(text,userid)
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
    # await button_handler(userid,action,setting)
    if action=='lang':
        global lang
        lang=setting

async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f"error occured {update} {context.error}")


def main(model_name):
    global model
    model=model_name
    print(f"using {model}")
    print("starting bot....")
    app=Application.builder().token(api_key).build()
    app.add_handler(CommandHandler("start",start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_handler(MessageHandler(filters.VOICE,handle_voice_message))
    app.add_error_handler(error)
    print("started polling.....")
    app.run_polling(poll_interval=3)