from glob import glob
from random import choice

from utils import get_smile, main_keyboard, play_random_number


def greet_user(update, context):
    print('Вызван /start')
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(
        f'Привет, пользователь! Ты вызвал команду /start {context.user_data["emoji"]}',
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_number(user_number)
        except(TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите целое число'
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_mem_image(update, context):
    mem_image_list = glob('/home/dkostarev/Рабочий стол/mems/*.jp*g')
    mem_image_name = choice(mem_image_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(mem_image_name, 'rb'),
                           reply_markup=main_keyboard())


def user_coordinates(update, context):
    coords = update.message.location
    update.message.reply_text(f'Ваши координаты {coords}!',
                              reply_markup=main_keyboard())
