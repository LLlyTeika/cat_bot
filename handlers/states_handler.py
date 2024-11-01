import utils
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from filters import CheckOp
from states import DefaultStates
from aiogram.types import Message
from keyboards.keyboard import create_keyboard

states_router = Router()


@states_router.message(DefaultStates.waiting_photo)
async def waiting_photo(message: Message, state: FSMContext) -> None:
    if message.photo:
        res = await utils.save_cat(message.from_user.id, message.photo[-1].file_id)
        if res:
            await message.answer("Сохранил.", reply_markup=create_keyboard(await utils.check_user_group(
                message.from_user.id
            )))
        else:
            await message.answer('изображение уже существует', reply_markup=create_keyboard(
                await utils.check_user_group(message.from_user.id)
            ))
        if not message.media_group_id:
            await state.clear()
            await utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
    else:
        await message.answer('я жду фото')


@states_router.message(DefaultStates.waiting_admin, lambda msg: utils.admin_state[msg.from_user.id] == 'admin')
async def waiting_add_admin(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        check_user = await utils.check_user_exists(int(message.text))
        if check_user:
            await utils.add_admin(int(message.text))
            await state.clear()
            await utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
        else:
            await message.answer('пользователя с таким айди не существует')
    else:
        await message.answer('айди состоит только из цифр\nдавай ещё раз')


@states_router.message(DefaultStates.waiting_admin, lambda msg: utils.admin_state[msg.from_user.id] == 'vip')
async def waiting_add_vip(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        check_user = await utils.check_user_exists(int(message.text))
        if check_user:
            await utils.add_vip(int(message.text))
            await state.clear()
            await utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
        else:
            await message.answer('пользователя с таким айди не существует')
    else:
        await message.answer('айди состоит только из цифр\nдавай ещё раз')


@states_router.message(DefaultStates.waiting_admin, lambda msg: utils.admin_state[msg.from_user.id] == 'delete')
async def waiting_delete_group(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        check_user = await utils.check_user_exists(int(message.text))
        if check_user:
            await utils.remove_admin(int(message.text))
            await state.clear()
            await utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
        else:
            await message.answer('пользователя с таким айди не существует')
    else:
        await message.answer('айди состоит только из цифр\nдавай ещё раз')


@states_router.message(DefaultStates.waiting_admin, lambda msg: utils.admin_state[msg.from_user.id] == 'give_id')
async def waiting_user_id(message: Message, state: FSMContext) -> None:
    check_user = await utils.check_user_exists(message.text)
    if check_user:
        user_id = await utils.give_user_id(message.text)
        await state.clear()
        await utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
        await message.answer(text=str(user_id))
    else:
        await message.answer('пользователя с таким тегом не существует')


@states_router.message(DefaultStates.waiting_user)
async def waiting_user(message: Message, state: FSMContext) -> None:
    user_tag = message.text
    albums = await utils.get_albums(user_tag)
    if albums:
        for album in albums:
            await message.answer_media_group(media=album)
        await state.clear()
        await utils.bot.delete_message(message.chat.id, utils.messages[message.from_user.id])
    elif albums is None:
        await message.answer('нет такого пользователя')
    else:
        await message.answer('у пользователя нет изображений')


