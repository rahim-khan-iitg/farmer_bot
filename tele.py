from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler
from dotenv import load_dotenv
import os
import requests
from src.TEXT import Gemini
from src.Bhashini.ASR import ASR
from src.Bhashini.bhashini_config import Languages
from src.settings import BotSettings

load_dotenv()
bot_username=os.getenv("BOT_USERNAME")
api_key=os.getenv("TELEGRAM_BOT_API_TOKEN")

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    reply_markup = BotSettings().SendLanguages(update)
    await update.message.reply_text("Please select the language:", reply_markup=reply_markup)
    await update.message.reply_text("Please select the chat mode:", reply_markup=BotSettings().SendChatMode(update))
    # await update.message.reply_text("hello my name is farmers bot how can i help you")

async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""""")


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
    res=requests.post("https://ffmpeg-audio-converter.vercel.app/convertBylink",{"url":file_path})
    data=res.json()
    asr=ASR()
    data=asr.from_base64(data['base64Wav'],'hindi')
    text=data['pipelineResponse'][0]['output'][0]['source']
    llm=Gemini()
    ans=llm.generete_ans(text)
    await update.message.reply_text(ans)

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    print(query.data)

async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f"error occured {update} {context.error}")


if __name__=="__main__":
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