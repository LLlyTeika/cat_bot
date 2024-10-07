import requests
from random import choice
from keyboards.keyboard import create_keyboard
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

default_router = Router()
api_cat_url = 'https://api.thecatapi.com/v1/images/search'
error_message = 'что-то пошло не так.'
answer_text_tu = ('держи', 'твой котик', 'прошу', 'пожалуйста')


@default_router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('привет, рад тебя видеть!', reply_markup=create_keyboard())


@default_router.message(lambda message: message.text == 'дай котика')
async def cat_handler(message: Message):
    cat_response = requests.get(api_cat_url)
    if cat_response.status_code == 200:
        await message.answer_photo(cat_response.json()[0]['url'], caption=choice(answer_text_tu))
    else:
        await message.answer(error_message)
