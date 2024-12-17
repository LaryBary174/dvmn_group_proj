import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests

bot = telebot.TeleBot('7808382160:AAHRd-iVztS4eVchkwbITXjp9o0QG3sJf2o')

BASE_URL = 'http://127.0.0.1:8000/api'



@bot.message_handler(commands=['start'])
def start(message):
    response = requests.get(f'{BASE_URL}/services/')
    response.raise_for_status()
    services = response.json()
    markup = InlineKeyboardMarkup(row_width=3)

    for service in services:
        markup.add(InlineKeyboardButton(
            text=service['title'],
            callback_data=service['id']
        ))

    bot.send_message(message.chat.id, "Пожалуйста выберите услугу для онлайн-записи", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_service_selection(call):
    service_id = call.data
    params = {
        'service_id': service_id,
    }
    response = requests.get(f'{BASE_URL}/specialists',params=params)
    response.raise_for_status()
    specialists = response.json()
    markup = InlineKeyboardMarkup()
    for specialist in specialists:
        markup.add(InlineKeyboardButton(
            text=specialist['name'],
            callback_data=f"{specialist['id']}"
        ))

    bot.send_message(call.message.chat.id,'Пожалуйста выберите мастера', reply_markup=markup)


bot.polling(none_stop=True)
