import logging

import telebot
import string
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save
from datetime import datetime
from itertools import zip_longest
from .models import UserProfile
from .models import Product
from .models import Order
from .models import Preference
from .models import Question
from .models import Contacts
from .models import ContactsLink
from .tasks import process_telegram_update
from .conf import bot
from bot.backend.commands import *

logger = logging.getLogger(__name__)

user_context = {}


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update_data = request.body.decode('utf-8')
            process_telegram_update.delay(update_data)
            logger.info(f"Отримане оновлення з webhook: {update_data}")
            return HttpResponse('')
        except Exception as e:
            logger.error(f"Помилка обробки вебхуку: {str(e)}")
