import requests
import states
import utils
import filters
from random import choice
from keyboards import keyboard, inline_keyboard
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

default_router = Router()
api_cat_url = 'https://api.thecatapi.com/v1/images/search'
error_message = 'что-то пошло не так.'
answer_text_tu = ('держи', 'твой котик', 'прошу', 'пожалуйста')


@default_router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('привет, рад тебя видеть!', reply_markup=keyboard.create_keyboard(
        await utils.check_admin(message.from_user.id)
    ))
    await state.clear()


@default_router.message(Command('admin'), filters.IsAdmin())
async def admin_handler(message: Message) -> None:
    temp = await message.answer('хочешь добавить администратора?',
                                reply_markup=inline_keyboard.admin_keyboard())
    utils.messages[message.from_user.id] = temp.message_id


@default_router.message(F.text == 'дай котика')
async def cat_handler(message: Message) -> None:
    cat_response = requests.get(api_cat_url)
    if choice(range(100)) == 1 and await utils.get_cats(message.from_user.id) is not None:
        photos = await utils.get_cats(message.from_user.id)
        await message.answer_photo(photo=choice(photos), caption=choice(answer_text_tu))
    elif cat_response.status_code == 200:
        await message.answer_photo(cat_response.json()[0]['url'], caption=choice(answer_text_tu))
    else:
        await message.answer(error_message)


@default_router.message(F.text == 'дай моего котика')
async def my_cat_handler(message: Message) -> None:
    photos = await utils.get_cats(message.from_user.id)
    if photos and photos is not None:
        await message.answer_photo(photo=choice(photos), caption=choice(answer_text_tu))
    else:
        await message.answer('у вас нет изображений :(')


@default_router.message(F.text == 'дай изображения другого пользователя')
async def other_cat_handler(message: Message, state: FSMContext) -> None:
    ReplyKeyboardRemove()
    kb = inline_keyboard.back()
    temp = await message.answer('введи тег', reply_markup=kb)
    utils.messages[message.from_user.id] = temp.message_id
    await state.set_state(states.DefaultStates.waiting_user)


@default_router.message(F.text == 'сохранить')
async def save_cat(message: Message, state: FSMContext) -> None:
    is_admin = await utils.check_admin(message.from_user.id)
    if is_admin:
        await state.set_state(states.DefaultStates.waiting_photo)
        temp = await message.answer("Дайте фото.\n\nесли сохраняете альбом - по завершению "
                                    "ткните кнопку \"назад\" под этим сообщением",
                                    reply_markup=inline_keyboard.back())
        utils.messages[message.from_user.id] = temp.message_id
    else:
        await message.answer("Вы не администратор.", reply_markup=keyboard.create_keyboard(
            utils.check_admin(message.from_user.id)
        ))


@default_router.message(F.text == 'удалить')
async def delete_cat(message: Message, state: FSMContext) -> None:
    is_admin = await utils.check_admin(message.from_user.id)
    if is_admin:
        utils.users_albums[message.from_user.id] = [await utils.get_albums(message.from_user.id),
                                                    0]  # список с альбомом и индексом пагинации
        album = utils.users_albums[message.from_user.id][0]
        if album:
            user_id = message.from_user.id
            utils.messages[message.from_user.id] = (await message.answer_media_group(media=album[0]),
                                                    await message.answer('выберите фото для удаления',
                                                                         reply_markup=inline_keyboard.album_keyboard(
                                                                             len(album[0]), user_id)))
        else:
            await message.answer('у вас нет изображений :(')
    else:
        await message.answer("Вы не администратор.", reply_markup=keyboard.create_keyboard(
            utils.check_admin(message.from_user.id)
        ))
