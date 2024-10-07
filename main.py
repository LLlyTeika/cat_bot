import asyncio
from aiogram import Bot, Dispatcher
from handlers import default_router
from config import Config


async def main():
    bot = Bot(token=Config.token)
    dp = Dispatcher(bot=bot)
    dp.include_router(default_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

