from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(text='добавить', callback_data='add_admin'),
            types.InlineKeyboardButton(text='удалить', callback_data='delete_group')
        ],
        [
            types.InlineKeyboardButton(text='vip', callback_data='vip_menu'),
        ],
        [
            types.InlineKeyboardButton(text='выйти', callback_data='exit')
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def vip_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(text='добавить', callback_data='add_vip'),
            types.InlineKeyboardButton(text='удалить', callback_data='delete_group')
        ],
        [
            types.InlineKeyboardButton(text='admin', callback_data='admin_menu')
        ],
        [
            types.InlineKeyboardButton(text='выйти', callback_data='exit')
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def exit_button():
    button = types.InlineKeyboardButton(text='выйти', callback_data='exit')
    return button


def exit_main():
    return types.InlineKeyboardMarkup(inline_keyboard=[[exit_button()]])


def album_keyboard(album_length: int, user_id: int):
    builder = InlineKeyboardBuilder()
    for i in range(album_length):
        builder.row(types.InlineKeyboardButton(text=str(i+1), callback_data=f'remove_photo_{user_id}_{i}'))
    builder.adjust(5)
    return builder.as_markup()
