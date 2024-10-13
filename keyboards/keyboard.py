from aiogram import types


def create_keyboard():
    keyboard = [
        [types.KeyboardButton(text='дай котика'), types.KeyboardButton(text='дай моего котика')],
        [types.KeyboardButton(text='сохранить')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    return keyboard




