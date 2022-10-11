from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def genmarkup_menu(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        markup.add(InlineKeyboardButton(i, callback_data = 'menu_'+i))
    return markup

def genmarkup_level(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        markup.add(InlineKeyboardButton(i, callback_data = 'level_'+i))
    markup.add(InlineKeyboardButton('Купить весь курс', callback_data='payment'))
    markup.add(InlineKeyboardButton('Начало', callback_data='start'))
    return markup



markup11 = InlineKeyboardMarkup().add(InlineKeyboardButton("ссылка для оплаты", callback_data="payment"))

