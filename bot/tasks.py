from celery import shared_task
from telebot import types
from .conf import bot
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_telegram_update(update_data):
    logger.info("Обробка оновлення Telegram")
    update = types.Update.de_json(update_data)
    logger.info(f"Отримане оновлення: {update}")
    bot.process_new_updates([update])
