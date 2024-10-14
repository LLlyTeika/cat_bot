import sqlite3
import aiosqlite
import logs
from aiogram import Bot

from config import Config

messages = {}
bot = Bot(token=Config.token)


async def check_user(username, user_id, user_full_name):
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        user_check = await cursor.execute('select * from users where id = ?', (user_id,))
        user_check = await user_check.fetchone()
        if not user_check:
            await cursor.execute('insert into users (id, full_name, tag) values (?, ?, ?)',
                                 (user_id, user_full_name, username))
            await db.commit()
            logs.new_user(username, user_id)


async def check_admin(user_id):
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        admin_check = await cursor.execute('select * from admins where id = ?', (user_id,))
        admin_check = await admin_check.fetchone()
        return admin_check is not None


async def add_admin(user_id):
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        await cursor.execute('insert into admins (id) values (?)', (user_id,))
        await db.commit()


async def remove_admin(user_id):
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        await cursor.execute('delete from admins where id = ?', (user_id,))
        await db.commit()


async def save_cat(user_id, photo_id):
    async with aiosqlite.connect("db.db") as db:
        try:
            cursor = await db.cursor()
            await cursor.execute('insert into users_cats (user_id, photo_id) values (?, ?)',
                                 (user_id, photo_id))
            await db.commit()
        except sqlite3.IntegrityError:
            await db.rollback()
            return False
        return True


async def get_cats(user_id):
    async with aiosqlite.connect("db.db") as db:
        cursor = await db.cursor()
        if user_id.isdigit():
            photos = await cursor.execute('SELECT uu.photo_id FROM users_cats '
                                          'uu WHERE uu.user_id = ?',
                                          (user_id,))
            photos = await photos.fetchone()
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
        return photos
