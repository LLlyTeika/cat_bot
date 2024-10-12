import aiosqlite
import logs


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


async def save_cat(user_id, photo_id):
    pass