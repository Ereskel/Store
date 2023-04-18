import asyncio
import logging

from aiogram.types import Message

from config import admins
from loader import dp, bot
from handlers import router1


async def notify(bot):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Мы уличные письки')


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    #    await bot.send_message(chat_id=admins, text = 'Мы уличные письки')
    await notify(bot)
    dp.include_router(router1)
    await dp.start_polling(bot)


# async def on_startup_notify(dp: Dispatcher):
#    for admin in admins:
#        try:
#            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")

#        except Exception as err:
#            logging.exception(err)


# async def notify(dp):
#    print('куку')
#    for admin in admins:
#        await dp.bot.send_message(chat_id=admin, text = 'Приветик')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
