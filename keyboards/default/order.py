from data import config
from aiogram import types
from utils.db_api import api_client
from utils.db_api.database import Tariffs


async def user_order(_user_data):
    lang = _user_data['lang']
    texts = config.Texts(lang)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        *[types.InlineKeyboardButton(text=f"✅{t['name']}" if t['id'] == _user_data['rate']['id'] else t['name'], callback_data=f"t{t['id']}") for t in _user_data['rates']],
    )
    markup.add(types.InlineKeyboardButton(text=await texts.services_text(), callback_data='none'))
    markup.add(
        *[types.InlineKeyboardButton(text=f"✅{s['name']}" if s['id'] in _user_data['selected_services'] else s['name'], callback_data=f"s{s['id']}") for s in _user_data["services"]]
    )
    bonus = await api_client.get_bonus(_user_data['phone'])
    markup.add(types.InlineKeyboardButton(text=await texts.use_bonus(), callback_data='none'))
    yes_no = await texts.yes_no()
    markup.add(types.InlineKeyboardButton(text=f"{'✅' if _user_data['use_bonuses'] == 'yes' else ''}{yes_no[0].split()[-1]}", callback_data='yes'), types.InlineKeyboardButton(text=f"{'✅' if _user_data['use_bonuses'] == 'no' else ''}{yes_no[1].split()[-1]}", callback_data='no'))
    markup.add(types.InlineKeyboardButton(text=await texts.comment_text(), callback_data='comment'))
    markup.add(types.InlineKeyboardButton(text=await texts.order(), callback_data='order_create'))


    return markup
