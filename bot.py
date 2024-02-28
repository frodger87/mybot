import logging
from random import randint, choice
from glob import glob

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize

import settings

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def greet_user(update, context):
    print('Вызван /start')
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f'Привет, пользователь! Ты вызвал команду /start {context.user_data["emoji"]}')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_number(user_number)
        except(TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите целое число'

    update.message.reply_text(message)


def play_random_number(user_number: int):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья:)'
    elif user_number < bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message


def send_mem_image(update, context):
    mem_image_list = glob('/home/dkostarev/Рабочий стол/mems/*.jpeg')
    mem_image_name = choice(mem_image_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(mem_image_name, 'rb'))




def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("mem", send_mem_image))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')

    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


if __name__ == '__main__':
    main()
