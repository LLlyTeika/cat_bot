from aiogram import types


def create_keyboard(group):
    keyboard = [
        [types.KeyboardButton(text='дай котика'), types.KeyboardButton(text='дай моего котика')],
        [types.KeyboardButton(text='дай изображения другого пользователя')]
    ]

    keyboard.append([
        types.KeyboardButton(text='сохранить'),
        types.KeyboardButton(text='удалить')
    ]) if group is not None and group in ('admin', 'vip') else None
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    return keyboard




