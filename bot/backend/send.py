import logging
import telebot
import string
import os
from .commands import *


logger = logging.getLogger(__name__)

user_context = {}


def send_order(message, chat_id, product, date, location, contact_info):
    try:
        caption = f"❗ Нове замовлення ❗\n"
        user = UserProfile.objects.get(telegram_id=chat_id)
        caption += f"👤 Користувач: {user.username}\n🤖 ID: {user.telegram_id}\n"
        caption += f"📦 Послуга: {product}\n"
        caption += f"🕰 Час: {date}\n"
        caption += f"📌 Локація: {location}\n"
        caption += f"📱 Контакти: {contact_info}\n"

        channel_id = -1002005268131
        bot.send_message(channel_id, caption)

        bot.send_message(chat_id, 'Дякую, до 10 хвилин менеджер зв\'яжеться з Вами!')
        start(message)
        clear_user_context(chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"При відправці виникла помилка: {str(e)}")


def send_question(message, chat_id, question):
    try:
        caption = f"❗ Запитання ❗\n"
        user = UserProfile.objects.get(telegram_id=chat_id)
        caption += f"👤 Користувач: {user.username}\n🤖 ID: {user.telegram_id}\n"
        caption += f"🔍 Номер: {question}\n"

        channel_id = -1002005268131
        bot.send_message(channel_id, caption)

        bot.send_message(chat_id, 'Дякую, до 10 хвилин менеджер зв\'яжеться з Вами!')
        start(message)
    except Exception as e:
        bot.send_message(chat_id, f"При відправці виникла помилка: {str(e)}")
