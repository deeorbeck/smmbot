import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from .functions import checkMember
from aiogram.dispatcher import FSMContext
from states.user import User
from utils.db_api import database



@dp.message_handler(content_types=['text'], state=User.survey,chat_type=types.ChatType.PRIVATE)
async def survey(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    if message.text != "Fikr bildirmayman hammasi yaxshi😎":
        await dp.bot.forward_message(chat_id=-1002067568042, from_chat_id=chat_id, message_id=message.message_id)
    if await database.Surveyers().search(chat_id=chat_id):
        await dp.bot.send_message(chat_id=chat_id,
                                  text="Siz avval bu so'rovnomada qatnashgansiz!\n/start")
        return
    await database.Surveyers().adduser(chat_id=chat_id)
    db = database.UsersTable()
    balance = int((await db.search(chat_id))[2])
    balance += 10_000
    await db.adduser(chat_id=chat_id, access=balance)

    await dp.bot.send_message(chat_id=chat_id, text="Sizga 10 000 so'm taqdim etildi!\n💸Hisobingizda {} so'm mavjud\n/start ni bosib davom eting.".format(balance))

