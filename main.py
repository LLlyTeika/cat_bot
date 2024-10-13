import logging
import asyncio
from middlewares.default_mid import LoggingMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from handlers import default_router, states_router
from config import Config


bot = Bot(token=Config.token)


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    dp.include_router(default_router)
    dp.include_router(states_router)
    dp.update.middleware(LoggingMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

