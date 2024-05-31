import asyncio
import os
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Menu: /start")
    print(message.message_id)


