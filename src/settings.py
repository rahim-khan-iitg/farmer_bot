from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from src.Bhashini.bhashini_config import Languages
from src.MYSQL.sql_handler import sql   

class BotSettings:
    def __init__(self) -> None:
        pass
    def SendLanguages(self)->InlineKeyboardMarkup:
        option=Languages.keys()
        keyboard=[[InlineKeyboardButton(text=opt,callback_data=opt + " lang")] for opt in option]
        keyboard_markup=InlineKeyboardMarkup(keyboard)
        return keyboard_markup

    def SendChatMode(self)->InlineKeyboardMarkup:
        keyboard=[[InlineKeyboardButton("General",callback_data="gen mode"),InlineKeyboardButton(text='Farmers Help',callback_data='fh mode')]]
        keyboard_markup=InlineKeyboardMarkup(keyboard)
        return keyboard_markup

async def button_handler(userid:int,action:str,setting):
    if action=="mode":
        sql().update_mode(userid,setting)
    if action=="lang":
        sql().update_lang(userid,setting)