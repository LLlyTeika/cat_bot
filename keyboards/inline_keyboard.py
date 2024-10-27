from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(text='добавить', callback_data='add_admin'),
            types.InlineKeyboardButton(text='назад', callback_data='back')
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def back_button():
    button = types.InlineKeyboardButton(text='назад', callback_data='back')
    return button


def back():
    return types.InlineKeyboardMarkup(inline_keyboard=[[back_button()]])


def album_keyboard(album_length: int, user_id: int):
    builder = InlineKeyboardBuilder()
    for i in range(album_length):
        builder.row(types.InlineKeyboardButton(text=str(i+1), callback_data=f'remove_photo_{user_id}_{i}'))
    builder.adjust(5)
    return builder.as_markup()
