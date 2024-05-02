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
from .conf import bot


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
        return HttpResponse('')
    return HttpResponse('Invalid request method')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    name = message.chat.username
    try:
        user = UserProfile.objects.get(telegram_id=chat_id)
        photo_path = os.path.join(os.getcwd(), 'bot_photo', 'photo_select.jpg')
        with open(photo_path, 'rb') as photo:
            clear_user_context(chat_id)
            bot.send_photo(chat_id, photo, reply_markup=create_reply_markup())
    except UserProfile.DoesNotExist:
        user = UserProfile.objects.create(telegram_id=chat_id, username=first_name, name=name)
        photo_path = os.path.join(os.getcwd(), 'bot_photo', 'photo_select.jpg')
        with open(photo_path, 'rb') as photo:
            clear_user_context(chat_id)
            bot.send_photo(chat_id, photo, reply_markup=create_reply_markup())


def create_reply_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton('🛞 Послуги'), KeyboardButton('Замовити послугу ✅'))
    markup.add(KeyboardButton('📄 Історія замовлень 📄'))
    markup.add(KeyboardButton('🥇 Переваги'), KeyboardButton('Контакти 📲'))
    markup.add(KeyboardButton('👩‍💻 Зв\'язатись з менеджером 👩‍💻'))
    return markup


user_context = {}


@bot.message_handler(func=lambda message: message.text == "🛞 Послуги")
def display_services(message):
    chat_id = message.chat.id
    products = Product.objects.all()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for product in products:
        markup.add(KeyboardButton(product.name))
    photo_path = os.path.join(os.getcwd(), 'bot_photo', 'photo_service.jpg')
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Замовити послугу ✅")
def order_service(message):
    chat_id = message.chat.id
    user_context[chat_id] = {'step': 'order_service'}
    products = Product.objects.all()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for product in products:
        markup.add(KeyboardButton(product.name))
    photo_path = os.path.join(os.getcwd(), 'bot_photo', 'photo_service.jpg')
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Замовити ✅")
def start_order(message):
    chat_id = message.chat.id
    if chat_id in user_context:
        product = user_context[chat_id]['product']
        if product:
            bot.send_message(chat_id, "Введіть точну дату та час! Наприклад: «Сьогодні 14:00»")
            user_context[chat_id]['product'] = product
            bot.register_next_step_handler(message, save_order_data, product)
        else:
            bot.send_message(chat_id, "Помилка: Спочатку оберіть послугу для замовлення.")
    else:
        bot.send_message(chat_id, "Помилка: Для початку оберіть послугу.")


@bot.message_handler(func=lambda message: message.text == "Назад 🔙")
def go_back(message):
    chat_id = message.chat.id
    clear_user_context(chat_id)
    bot.send_message(chat_id, "Меню", reply_markup=create_reply_markup())


@bot.message_handler(func=lambda message: message.text in [product.name for product in Product.objects.all()])
def choose_product(message):
    chat_id = message.chat.id
    text = message.text
    product = Product.objects.get(name=text)
    if product:
        if chat_id in user_context:
            user_context[chat_id]['product'] = product
            user_context[chat_id]['step'] = 'order_service'
            bot.send_message(chat_id, "Введіть точну дату та час! Наприклад: «Сьогодні 14:00»")
            bot.register_next_step_handler(message, save_order_data, product)
        else:
            user_context[chat_id] = {'product': product, 'step': 'order_service'}
            question = product.question
            bot.send_message(chat_id, question)
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            markup.add(KeyboardButton("Замовити ✅"))
            markup.add(KeyboardButton("Назад 🔙"))
            photo_path = os.path.join(os.getcwd(), 'bot_photo', 'photo_select.jpg')
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, reply_markup=markup)
    else:
        bot.send_message(chat_id, "Послуга не знайдена. Будь ласка, виберіть іншу.")


def save_order_data(message, product):
    chat_id = message.chat.id
    user_input = message.text
    try:
        user = UserProfile.objects.get(telegram_id=chat_id)
        user_context[chat_id]['user'] = user
        user_context[chat_id]['date'] = user_input
        user_context[chat_id]['product'] = product # Додайте product до контексту користувача
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Поділитись геолокацією", request_location=True))
        markup.add(KeyboardButton("Написати"))
        bot.send_message(chat_id, "Вкажіть спосіб вказання місцезнаходження:", reply_markup=markup)

    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")



@bot.message_handler(func=lambda message: message.text == "Написати")
def write_location(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введіть місцезнаходження")
    bot.register_next_step_handler(message, save_order_location_text)


@bot.message_handler(content_types=['location'])
def save_order_location(message):
    chat_id = message.chat.id
    location = message.location
    try:
        latitude = location.latitude
        longitude = location.longitude
        location_text = f"{latitude}, {longitude}"
        user = user_context[chat_id]['user']
        date = user_context[chat_id]['date']
        product = user_context[chat_id]['product']
        user_context[chat_id]['location'] = location_text
        order = Order.objects.create(user=user, product=product, date=date, location=location_text)
        order.save()

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Поділитись контактом", request_contact=True))
        markup.add(KeyboardButton("Написати самостійно"))
        bot.send_message(chat_id, "Надішліть контактні дані:", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


def save_order_location_text(message):
    chat_id = message.chat.id
    location = message.text
    try:
        user = user_context[chat_id]['user']
        date = user_context[chat_id]['date']
        product = user_context[chat_id]['product']
        user_context[chat_id]['location'] = location
        order = Order.objects.create(user=user, product=product, date=date, location=location)
        order.save()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Поділитись контактом", request_contact=True))
        markup.add(KeyboardButton("Написати самостійно"))
        bot.send_message(chat_id, "Надішліть контактні дані:", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    contact = message.contact
    try:
        if "step" in user_context.get(chat_id, {}) and user_context[chat_id]["step"] == "order_service":
            save_order_contact(message, chat_id, contact.phone_number)
        else:
            save_question_contact(message, chat_id, contact)
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


def save_order_contact(message, chat_id, contact_info):
    user = user_context[chat_id]['user']
    date = user_context[chat_id]['date']
    product = user_context[chat_id]['product']
    location = user_context[chat_id]['location']
    order = Order.objects.filter(user=user, product=product, date=date, location=location).last()
    order.contact = contact_info
    order.save()
    send_order(message, chat_id, order.product, order.date, order.location, contact_info)


def save_question_contact(message, chat_id, contact):
    try:
        user_profile = UserProfile.objects.get(telegram_id=chat_id)
        question = contact.phone_number
        question_obj = Question.objects.create(user=user_profile, question=question)
        send_question(message, chat_id, question_obj.question)
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


@bot.message_handler(func=lambda message: message.text == "Написати самостійно")
def write_contact(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введіть контактні дані")
    bot.register_next_step_handler(message, save_orders_contact)


def save_orders_contact(message):
    chat_id = message.chat.id
    contact_info = message.text
    try:
        user = user_context[chat_id]['user']
        date = user_context[chat_id]['date']
        product = user_context[chat_id]['product']
        location = user_context[chat_id]['location']
        order = Order.objects.filter(user=user, product=product, date=date, location=location).last()
        order.contact = contact_info
        order.save()
        send_order(message, chat_id, order.product, order.date, order.location, contact_info)
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


def clear_user_context(chat_id):
    if chat_id in user_context:
        del user_context[chat_id]


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


@bot.message_handler(func=lambda message: message.text == "📄 Історія замовлень 📄")
def order_history(message):
    chat_id = message.chat.id
    display_order_history(chat_id)


def display_order_history(chat_id):
    try:
        orders = Order.objects.filter(user__telegram_id=chat_id)
        if orders:
            message = "Ваша історія замовлень:\n\n"
            for order in orders:
                message += f"Замовлення #{order.id}:\n"
                message += f"Послуга: {order.product}\n"
                message += f"Дата: {order.date}\n"
                message += f"Місцезнаходження: {order.location}\n"
                message += f"Контакт: {order.contact}\n\n"
            bot.send_message(chat_id, message)
        else:
            bot.send_message(chat_id, "У вас ще немає замовлень.")
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


@bot.message_handler(func=lambda message: message.text == "🥇 Переваги")
def display_preferences(message):
    chat_id = message.chat.id
    try:
        preferences = Preference.objects.all()
        if preferences:
            preference_text = ""
            for preference in preferences:
                preference_text += f"{preference.preference}\n"
            bot.send_message(chat_id, preference_text)
        else:
            bot.send_message(chat_id, "На жаль, переваги не знайдено.")
    except Exception as e:
        bot.send_message(chat_id, f"Помилка: {str(e)}")


@bot.message_handler(func=lambda message: message.text == "Контакти 📲")
def contacts(message):
    contacts = Contacts.objects.all()
    for contact in contacts:
        message_text = f"{contact.text}\n"
        inline_markup = types.InlineKeyboardMarkup()
        links = ContactsLink.objects.filter(contact=contact)
        for link in links:
            inline_btn = types.InlineKeyboardButton(text=link.name, url=link.links)
            inline_markup.add(inline_btn)
        bot.send_message(message.chat.id, message_text, reply_markup=inline_markup)


@bot.message_handler(func=lambda message: message.text == "👩‍💻 Зв\'язатись з менеджером 👩‍💻")
def question(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton("Поділитись контактами", request_contact=True))
    markup.add(KeyboardButton("Написати контакти"))
    photo_path = os.path.join(os.getcwd(), 'bot_photo', 'photo_contacts.jpg')
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Написати контакти")
def write_contact(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введіть контактні дані")
    bot.register_next_step_handler(message, save_contact)


def save_contact(message):
    chat_id = message.chat.id
    user_profile = UserProfile.objects.get(telegram_id=chat_id)
    questions = message.text
    contact_obj = Question.objects.create(user=user_profile, question=questions)
    send_question(message, chat_id, contact_obj.question)


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
