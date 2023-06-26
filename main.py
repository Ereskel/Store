import asyncio
import logging

from aiogram.types import Message

from config import admins
from loader import dp, bot
from handlers import router1


async def notify(bot):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Бот запущен')


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    #    await bot.send_message(chat_id=admins, text = 'Мы уличные письки')
    await notify(bot)
    dp.include_router(router1)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
