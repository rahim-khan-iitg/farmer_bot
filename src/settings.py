from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.Bhashini.bhashini_config import Languages

class BotSettings:
    def __init__(self) -> None:
        pass
    def SendLanguages(self,update:Update)->InlineKeyboardMarkup:
        option=Languages
        user=update.effective_user.username
        keyboard=[[InlineKeyboardButton(text=opt,callback_data=Languages[opt] + " lang "+user)] for opt in option]
        keyboard_markup=InlineKeyboardMarkup(keyboard)
        return keyboard_markup

    def SendChatMode(self,update:Update)->InlineKeyboardMarkup:
        user=update.effective_user.username
        keyboard=[[InlineKeyboardButton("General",callback_data="gen mode "+user),InlineKeyboardButton(text='Farmers Help',callback_data='fh mode '+user)]]
        keyboard_markup=InlineKeyboardMarkup(keyboard)
        return keyboard_markup