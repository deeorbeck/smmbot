import asyncio
import os
import time
from loader import  bot
from data import config
from aiogram import types
from utils.db_api import database
import re
import string
from random import choices
import json
from keyboards.default.all import menu_markup
from utils.db_api.database import UsersTable, TokensTable
from string import ascii_letters
from random import choices
from datetime import datetime as dt
from states.user import User
import pandas as pd


async def db_to_excel(id, caption):
    users = await database.UsersTable().search(all=True)
    chat_ids = []
    names = []
    languages = []
    access_dates = []
    reffers = []
    last_usages = []

    for u in users:
        chat_id = u[0]
        name = None
        lang = u[1]
        access = u[2]
        reffer_by = u[3]
        last_usage = None
        user = await database.ExtraTable().search(chat_id=chat_id)
        if user:
            name = user[1]
            last_usage = user[2]
        chat_ids.append(chat_id)
        names.append(name)
        languages.append(lang)
        access_dates.append(access)
        reffers.append(reffer_by)
        last_usages.append(last_usage)
    data = {
        'chat_id': chat_ids,
        'Full Name': names,
        'Language': languages,
        'Access Date': access_dates,
        'Reffer By': reffers,
        'Last Usage': last_usages
    }
    df = pd.DataFrame(data)
    output = f"{dt.now().second}.xlsx"
    df.to_excel(output)
    await bot.send_chat_action(id, types.ChatActions.UPLOAD_DOCUMENT)
    await bot.send_document(chat_id=id,document=open(output, 'rb'), caption=caption)
    await asyncio.sleep(10)
    os.remove(output)




async def generate_token():
    letters = ascii_letters + "1234567890"
    token = "".join(choices(letters, k=9))
    while await TokensTable().search(token=token):
        token = "".join(choices(letters, k=9))
    return token

async def list_tokens(days):
    db = TokensTable()
    tokens = await db.search(days=days)
    txt = f"<b>Umumiy tokenlar soni: {len(tokens)} ta</b>\n"
    count = 1
    for token in tokens:
        txt += f"{count}. <code>{token[0]}</code> \n"
        count += 1
    return txt
def to_markdown(text):
  # text = text.replace("**", '@@').replace('*', "@@").replace("@@", "**")
  text = text.replace("*", '')
  return text



async def password_render():
    letters = string.ascii_letters + string.digits + string.punctuation
    return "".join(choices(letters, k=8))
async def checkMember(user_id, lang):
    texts = config.Texts(lang)
    db = database.UsersTable()
    channels = await db.search(all=True)
    markup = types.InlineKeyboardMarkup(row_width=1)
    number = 1
    for ch in channels:
        ch = ch[0]
        try:
            chat = await bot.get_chat(ch)
            d = await bot.get_chat_member(ch, user_id)
        except:
            db = database.UsersTable()
            await db.delete(ch)
            continue
        if d['status'] == "left":
            txt = await texts.channel_number()
            markup.add(
                types.InlineKeyboardButton(text=txt.format(number), url=f"{chat['invite_link']}")
            )
            number += 1
    if markup['inline_keyboard']:
        markup.add(types.InlineKeyboardButton(text=await texts.confirm_joined(), callback_data='confirm_joined'))
    return markup
async def check_number(number):
    number = str(number)
    if len(number) != 13:
          return False
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    return re.match(validate_phone_number_pattern, number)
async def is_same_locations(_user_data):
    return _user_data['lat'] == _user_data['lat1'] and _user_data['long'] == _user_data['long1']


