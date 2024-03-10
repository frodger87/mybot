import os
from glob import glob
from random import choice

from utils import get_smile, main_keyboard, play_random_number, \
    has_object_in_image


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


def check_user_photo(update, context):
    update.message.reply_text('Обрабатываю фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(file_name)
    if has_object_in_image(file_name, 'cat'):
        update.message.reply_text('Обнаружен котик, сохраняю в библиотеку.')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpeg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Тревога! Котик не обнаружен.')
