from src.utils import *

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