from time import sleep

import telebot

TOKEN = '6452560014:AAEW22uvw4bMEU5FWVUBvRgbfnHbqdnyxzE'

bot = telebot.TeleBot(TOKEN)


def set_webhook():
    from django.conf import settings
    bot.remove_webhook()
    bot.set_webhook(url=settings.WEBHOOK_URL)