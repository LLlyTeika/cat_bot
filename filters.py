from aiogram.types import TelegramObject
from aiogram.filters import BaseFilter
import utils
import logging


class IsAdmin(BaseFilter):
    async def __call__(self, msg: TelegramObject) -> bool:
        logging.info(f'запрос админки: {msg.from_user.id}, {msg.from_user.username}')
        check_result = await utils.check_admin(msg.from_user.id)
        logging.info('доступ разрешен' if check_result else 'доступ запрещен')
        return check_result
