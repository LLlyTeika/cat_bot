from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='дай котика')
    keyboard_builder.button(text='сохранить')
    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup(resize_keyboard=True)
