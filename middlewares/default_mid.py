from aiogram import BaseMiddleware
from aiogram.types import Update
from utils import check_user
import logs


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            user_name = event.message.from_user.username
            user_id = event.message.from_user.id
            user_full_name = event.message.from_user.full_name
            logs.take_message(user_name)
            await check_user(user_name, user_id, user_full_name)

        return await handler(event, data)
