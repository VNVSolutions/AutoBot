from time import sleep

import telebot
from django.conf import settings

TOKEN = '6452560014:AAEW22uvw4bMEU5FWVUBvRgbfnHbqdnyxzE'

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot(TOKEN)


# Встановлюємо вебхук
bot.remove_webhook()
bot.set_webhook(url=settings.WEBHOOK_URL)