import logging
import utils
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states import DefaultStates
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto
from keyboards.keyboard import create_keyboard

states_router = Router()


@states_router.message(DefaultStates.waiting_photo)
async def waiting_photo(message: Message, state: FSMContext) -> None:
    if message.photo:
        res = await utils.save_cat(message.from_user.id, message.photo[-1].file_id)
        if res:
            await message.answer("Сохранил.", reply_markup=create_keyboard())
            await state.clear()
        else:
            await message.answer('изображение уже существует', reply_markup=create_keyboard())
    else:
        await message.answer('я жду фото')


@states_router.message(DefaultStates.waiting_admin)
async def waiting_admin(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await utils.add_admin(int(message.text))
        await state.clear()
        utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
    else:
        await message.answer('айди состоит только из цифр\nдавай ещё раз')


@states_router.message(DefaultStates.waiting_user)
async def waiting_user(message: Message, state: FSMContext) -> None:
    tag = message.text
    photos = await utils.get_cats(tag)
    if photos:
        for i in range(len(photos)//10+1):
            album = []
            for j in range(10):
                if len(photos) <= i*10+j:
                    break
                else:
                    album.append(InputMediaPhoto(media=photos[i*10+j][0]))
            await message.answer_media_group(media=album)
    elif photos is None:
        await message.answer('нет такого пользователя')
    else:
        await message.answer('у пользователя нет изображений')


