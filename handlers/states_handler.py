from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states import DefaultStates
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.keyboard import create_keyboard

states_router = Router()


@states_router.message(DefaultStates.waiting)
async def waiting(message: Message, state: FSMContext):
    if message.photo:
        pass
    else:
        await message.answer('я жду фото')
    await state.clear()
    await message.answer("Сохранил.", reply_markup=create_keyboard())
