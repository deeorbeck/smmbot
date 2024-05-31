from aiogram import executor, types
from loader import dp
import middlewares, filters, handlers, utils
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import setup_tables, UsersTable, Surveyers
from data import config
from datetime import datetime as dt


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
