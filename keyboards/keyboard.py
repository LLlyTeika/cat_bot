from aiogram import types


def create_keyboard(admin_check):
    keyboard = [
        [types.KeyboardButton(text='дай котика'), types.KeyboardButton(text='дай моего котика')],
        [types.KeyboardButton(text='дай изображения другого человека')]
    ]

    keyboard.append([types.KeyboardButton(text='сохранить')]) if admin_check else None
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    return keyboard




