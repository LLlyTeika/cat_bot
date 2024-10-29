import sqlite3
import aiosqlite
import logs
from aiogram import Bot
from aiogram.types import InputMediaPhoto

from config import Config

messages = {}
users_albums = {}
bot = Bot(token=Config.token)


async def check_user(username, user_id, user_full_name) -> None:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        user_check = await cursor.execute('select * from users where id = ?', (user_id,))
        user_check = await user_check.fetchone()
        if not user_check:
            await cursor.execute('insert into users (id, full_name, tag, user_group) values (?, ?, ?, ?)',
                                 (user_id, user_full_name, username, 'user'))
            await db.commit()
            logs.new_user(username, user_id)


async def check_user_group(user_id) -> str | None:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        user_group = await cursor.execute('select user_group from users where id = ?', (user_id,))
        user_group = await user_group.fetchone()
        return user_group[0]


async def add_admin(user_id) -> None:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        await cursor.execute('insert into admins (id) values (?)', (user_id,))
        await db.commit()


async def remove_admin(user_id) -> None:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        await cursor.execute('delete from admins where id = ?', (user_id,))
        await db.commit()


async def save_cat(user_id, photo_id) -> bool:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        try:
            await cursor.execute('insert into users_cats (user_id, photo_id) values (?, ?)',
                                 (user_id, photo_id))
            await db.commit()
        except sqlite3.IntegrityError:
            await db.rollback()
            return False
    return True


async def remove_cat(photo_id, user_id) -> None:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        await cursor.execute('delete from users_cats where photo_id = ? and user_id = ?',
                             (photo_id, user_id))
        await db.commit()


async def get_cats(user_id) -> list[str] | None:
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        if isinstance(user_id, int):
            photos = await cursor.execute('SELECT uu.photo_id FROM users_cats '
                                          'uu WHERE uu.user_id = ?',
                                          (user_id,))
            photos = await photos.fetchall()
        else:
            user_id = user_id[1:] if user_id.startswith('@') else user_id
            uid = await cursor.execute('select id from users where tag = ?', (user_id,))
            uid = await uid.fetchone()
            if uid is not None:
                photos = await cursor.execute('SELECT uu.photo_id FROM users_cats '
                                              'uu where uu.user_id = ?',
                                              (uid[0],))
                photos = list(await photos.fetchall())
                photos = photos if len(photos) > 0 else []
            else:
                return None
        photos = [photo[0] for photo in photos]
        return photos


async def get_albums(user_tag) -> list[list[InputMediaPhoto]] | None:
    photos = await get_cats(user_tag)
    albums = []
    if photos:
        for i in range(len(photos) // 10 + 1):
            album = []
            for j in range(10):
                if len(photos) <= i * 10 + j:
                    break
                else:
                    album.append(InputMediaPhoto(media=photos[i * 10 + j]))
            if album:
                albums.append(album)
    elif photos is None:
        albums = None
    return albums


def largest_zip(li1: list | tuple, li2: list | tuple) -> list[tuple]:
    return [(li1[i] if len(li1) > i else None, li2[i] if len(li2) > i else None, i)
            for i in range(max(len(li1), len(li2)))]
