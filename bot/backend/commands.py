import logging

import telebot
import string
import os
from bot.views import *
from .handler import *

user_context = {}


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    username = message.chat.username
    try:
        user, created = UserProfile.objects.get_or_create(telegram_id=chat_id, defaults={'username': first_name, 'name': username})
        clear_user_context(chat_id)
        bot.send_message(chat_id, "Оберіть дію 👇", reply_markup=create_reply_markup())
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")