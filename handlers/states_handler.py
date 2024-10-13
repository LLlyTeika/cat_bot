import logging
import utils
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states import DefaultStates
from aiogram.types import Message, ReplyKeyboardRemove
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

