from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from keyboards.inline_keyboard import album_keyboard
from aiogram.exceptions import TelegramBadRequest

import states
import utils
from keyboards import inline_keyboard

callback_router = Router()


@callback_router.callback_query(F.data == 'exit')
async def exit_main(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.delete()


@callback_router.callback_query(F.data == 'add_admin')
async def add_admin(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.DefaultStates.waiting_admin)
    utils.admin_state[call.from_user.id] = 'admin'
    back_button = inline_keyboard.exit_main()
    await call.message.edit_text('отлично!\n\nвведи id администратора для добавления',
                                 reply_markup=back_button)


@callback_router.callback_query(F.data == 'add_vip')
async def add_vip(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.DefaultStates.waiting_admin)
    utils.admin_state[call.from_user.id] = 'vip'
    back_button = inline_keyboard.exit_main()
    await call.message.edit_text('хочешь добавить випа?',
                                 reply_markup=back_button)


@callback_router.callback_query(F.data == 'delete_group')
async def delete_group(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.DefaultStates.waiting_admin)
    utils.admin_state[call.from_user.id] = 'delete'
    back_button = inline_keyboard.exit_main()
    await call.message.edit_text('отлично!\n\nвведи id пользователя для удаления',
                                 reply_markup=back_button)


@callback_router.callback_query(F.data == 'vip_menu')
async def vip_menu(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text('хочешь добавить випа?',
                                 reply_markup=inline_keyboard.vip_keyboard())


@callback_router.callback_query(F.data == 'give_id')
async def give_id(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.DefaultStates.waiting_admin)
    utils.admin_state[call.from_user.id] = 'give_id'
    await call.message.edit_text('отлично!\n\nвведи тег пользователя для получения id',
                                 reply_markup=inline_keyboard.exit_main())


@callback_router.callback_query(F.data == 'admin_menu')
async def admin_menu(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.DefaultStates.waiting_admin)
    utils.admin_state[call.from_user.id] = 'user_id'
    await call.message.edit_text('хочешь добавить админа?',
                                 reply_markup=inline_keyboard.admin_keyboard())


@callback_router.callback_query(F.data.startswith('remove_photo'))
async def remove_photo(call: CallbackQuery, state: FSMContext) -> None:
    # получаем индекс картинки в альбоме и id пользователя
    button_id, user_id = int(call.data.split('_')[-1]), int(call.data.split('_')[-2])
    # получаем страницу в альбоме
    pagination = utils.users_albums[user_id][1]
    # список картинок пользователя (разом все. это не альбом)
    photos = await utils.get_cats(user_id)
    # удаляем изображение в базе
    await utils.remove_cat(photos[button_id+10*pagination], user_id)
    # получаем обновлённый альбом
    albums = await utils.get_albums(user_id)
    # список сообщений, который отправил бот юзеру
    usr_photos: list[Message] = utils.messages[user_id][0]
    # переписываем дефолтный зип
    zip = utils.largest_zip
    # цикл перебора сообщения, подмена/удаления изображения в альбоме
    if albums:
        for msg, photo, index in zip(usr_photos, albums[pagination]):
            if msg and photo:
                try:
                    await msg.edit_media(media=photo)
                except TelegramBadRequest:
                    continue
            elif photo is None:
                await utils.messages[user_id][0][index].delete()
                del utils.messages[user_id][0][index]
        album_len = len(albums[pagination])
        await utils.messages[user_id][1].edit_text('выберите фото для удаления', reply_markup=album_keyboard(
            album_len, user_id))
    else:
        await utils.messages[user_id][0][0].delete()
        await utils.messages[user_id][1].edit_text('нет фото :(', reply_markup=None)
    await call.answer()


