from data import config
from aiogram import types
from utils.db_api.database import TariffsTable
async def tariffs_key():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(*[types.KeyboardButton(text=t[0]) for t in  await TariffsTable().search(all=True)])
    return m

async def admin_menu_key(lang):
    texts = config.Texts(lang)
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    m.add(
        *[
            types.KeyboardButton(text=b) for b in config.Texts(lang).admin_sections()
        ]

    )
    return m

def menu_markup(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        *[types.KeyboardButton(i) for i in config.Texts(lang).user_sections()]
    )
    return markup

async def informations_key(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        *[types.KeyboardButton(i) for i in await config.Texts(lang).information_sections()]
    )
    return markup
def cities(data_list, sort_by_row = False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if sort_by_row:
        for i in data_list:
            markup.add(types.KeyboardButton(text=i))
    else:
        markup.add(
            *[types.KeyboardButton(i) for i in data_list]
        )
    return markup


def cities_inline(data_list):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(
        *[types.KeyboardButton(i) for i in data_list]
    )
    return markup
