from random import randint, choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


def main_keyboard():
    return ReplyKeyboardMarkup(
        [['Хочу мем', KeyboardButton('Мои координаты', request_location=True)]])


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def play_random_number(user_number: int):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья:)'
    elif user_number < bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message
