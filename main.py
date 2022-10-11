import logging
import pathlib
import sqlite3
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Keyboards import genmarkup_menu, genmarkup_level, markup11
from PathSource import list_of_course_name, list_of_course_path, list_course_level_name

conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER UNIQUE, username TEXT)')



class FsmBot(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()


API_TOKEN = os.getenv('TOKEN')
admins = [304128276, 886880023, 30825880]
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
chat_support_id = -1001749197487


def find_file(fileDir, fileExtr):
    return list(pathlib.Path(fileDir).glob(fileExtr))


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.from_user.username
        data['user_id'] = message.from_user.id

        try:
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(
                f'INSERT OR IGNORE INTO users(user_id, username) VALUES("{message.from_user.id}", "@{message.from_user.username}")')
            conn.commit()
        except Exception as e:
            print(e)

    msg_txt = f"""Здравствуй, {message.from_user.first_name}\n
        Рады видеть вас в нашем боте учебников.Обязательно подписывайтесь, ассортимент будет пополняться 🥰 По всем вопросам обращайтесь @eng_booksbott"""
    await message.answer(msg_txt, reply_markup=genmarkup_menu(list_of_course_name))


@dp.callback_query_handler(text='start')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    await query.message.reply('Меню', reply_markup=genmarkup_menu(list_of_course_name))


@dp.callback_query_handler(text_contains='menu_')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data[5:]
    menu_ind = list_of_course_name.index(answer_data)
    async with state.proxy() as data:
        data['ind'] = menu_ind
    await query.answer(f'You answered with {answer_data!r}')
    for i in list_of_course_name:
        if answer_data.__contains__(i):
            with open(pathlib.Path(list_of_course_path[menu_ind], 'Description.txt'), encoding="utf-8") as f:
                kurs_txt = f.read()
            photo = open(find_file(pathlib.Path(list_of_course_path[menu_ind]), r'*.jpg')[0], 'rb')

            await query.message.answer_photo(photo)
            await query.message.answer(f"Выбран курс {kurs_txt}", reply_markup=genmarkup_level(
                list_course_level_name[menu_ind]))


@dp.callback_query_handler(text_contains='level_')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        menu_ind = data['ind']
    answer_data = query.data[6:]
    path_level = pathlib.Path(list_of_course_path[menu_ind], answer_data)
    await query.answer('ok')
    photo = open(find_file(path_level, r'*.jpg')[0], 'rb')
    doc = open(find_file(path_level, r'*.pdf')[0], 'rb')
    await query.message.answer_photo(photo)
    await query.message.answer_document(doc)
    await query.message.answer(f"По всем вопросам обращайтесь @eng_booksbott",
                               reply_markup=markup11,
                               parse_mode="HTML")


@dp.callback_query_handler(text='payment')
async def fff(query: types.CallbackQuery, state: FSMContext):
    text = '<a href="http://qiwi.com/n/ENGLISHBOOKS">ссылке</a>'
    await query.message.answer(f"Чтобы оплатить курс перейдите по {text} ,"
                               f" мы увиди оплату и отправим с аккаунта ссылку на яндекс диск ",
                               parse_mode="HTML")
    async with state.proxy() as data:
        user_name = data['user_name']
        user_id = data['user_id']
    await bot.send_message(chat_support_id, f"'Этот пользователь дошел до оплаты @{user_name}, {user_id}")


@dp.message_handler(commands=['profile'])
async def get_profile(msg: types.Message):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users')
    result = cur.fetchall()
    await bot.send_message(msg.from_user.id, f'{result}')


@dp.message_handler(commands=['sendfile'])
async def get_profile(msg: types.Message, state: FSMContext):
    if msg.from_user.id in admins:
        await bot.send_message(msg.from_user.id, "введи id чела кому отправить и ссылку на файл через пробел")
        await FsmBot.state2.set()
    else:
        await bot.send_message(msg.from_user.id, "только админ может")


@dp.message_handler(state=FsmBot.state2)
async def get_profile(message: types.Message, state: FSMContext):
    try:
        a1 = message.text.split()
        await bot.send_message(chat_id=a1[0], text=a1[1])
        await state.reset_state()

    except BaseException:
        await bot.send_message(message.from_user.id, 'некоректные данные попробуй еще разок')


@dp.message_handler(commands=['sendupdate'])
async def set_update(msg: types.Message):
    if msg.from_user.id in admins:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM users')
        users = cur.fetchall()
        for user in users:
            print(user)
            try:
                await bot.send_message(user[0], "вышло обновление,проверь наши новые предложения")
            except BaseException:
                pass

    else:
        await bot.send_message(msg.from_user.id, "только админ может")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
