import logging

import telebot
import string
import os
from .commands import *


def create_reply_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton('🛞 Ознайомитись з послугою'), KeyboardButton('Замовити послугу ✅'))
    markup.add(KeyboardButton('📄 Історія замовлень 📄'))
    markup.add(KeyboardButton('🥇 Переваги'), KeyboardButton('Контакти 📲'))
    markup.add(KeyboardButton('👩‍💻 Зв\'язатись з менеджером 👩‍💻'))
    print("Кнопки меню markup")
    print(markup)
    return markup