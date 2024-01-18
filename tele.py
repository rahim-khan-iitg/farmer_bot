from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from dotenv import load_dotenv
import os
import requests
from src.TEXT import Gemini
from src.Bhashini.ASR import AudioConverter

load_dotenv()
bot_username=os.getenv("BOT_USERNAME")
api_key=os.getenv("TELEGRAM_BOT_API_TOKEN")

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello my name is farmers bot how can i help you")

async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("let me know what do you want??")


async def custom_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is the custom command message")


def handle_response(text:str)->str:
    processed=text.lower()
    llm=Gemini()
    ans=llm.generete_ans(processed)
    return ans

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str=update.message.text
    print(update)
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
    file=await message.get_file()
    file_path=file.file_path
    res=requests.get(file_path)
    converter=AudioConverter()
    x=converter.convert_ogg_to_wav_base64(res.content)
    print(x)
    await update.message.reply_voice(res.content)

async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f"error occured {update} {context.error}")


if __name__=="__main__":
    print("starting bot....")
    app=Application.builder().token(api_key).build()
    app.add_handler(CommandHandler("start",start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_handler(MessageHandler(filters.VOICE,handle_voice_message))

    app.add_error_handler(error)


    print("started polling.....")
    app.run_polling(poll_interval=3)