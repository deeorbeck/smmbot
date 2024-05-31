import logging
from aiogram import Dispatcher
from data.config import SUPER_ADMIN


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(SUPER_ADMIN, "🤖Bot is running...🚀")
    except Exception as err:
        logging.exception(err)
