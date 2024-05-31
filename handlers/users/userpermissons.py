from utils.db_api import database
from loader import dp
from states.user import User
from datetime import datetime as dt
from data import config
from keyboards.inline.all import getTariffs
from aiogram import types


async def is_member_all_chats(_user_data):
    chat_id = _user_data['chat_id']
    lang = _user_data['lang']
    texts = config.Texts(lang)
    db = database.ChannelsTable()
    channels = await db.search(all=True)
    for ch in channels:
        try:
            user = await dp.bot.get_chat_member(ch[0], chat_id)
            if user['status'] == 'left':
                m = types.InlineKeyboardMarkup(row_width=1)
                for ch in channels:
                    chat = await dp.bot.get_chat(ch[0])
                    m.add(types.InlineKeyboardButton(text=chat.title, url=chat.username))
                m.add(types.InlineKeyboardButton(text=texts.subscibed(), callback_data='followed'))
                txt = texts.beforemustsubscribe()
                await dp.bot.send_message(chat_id=chat_id, text=txt, reply_markup=m)
                await User.confirm_joined.set()
                return False
        except: pass
    return True

