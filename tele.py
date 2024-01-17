from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
bot_username=os.getenv("BOT_USERNAME")
api_key=os.getenv("TELEGRAM_BOT_API_TOKEN")

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello my name is farmers bot how can i help you")


def handle_response(text:str)->str:
    processed=text.lower()

    if "hello" in processed:
        return "hey there"
    else:
        return "command not found"
    

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str=update.message.text
    print(f"{update.message.chat_id} {message_type} {text}")


if __name__=="__main__":
    print("starting bot....")
    app=Application.builder().token(api_key).build()
    app.add_handler(CommandHandler("start",start_command))
    print("started polling.....")
    app.run_polling(poll_interval=3)