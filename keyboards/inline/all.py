from aiogram import types
from utils.db_api.database import TariffsTable

async def getTariffs():
    db = TariffsTable()
    tariffs = await db.search(all=True)
    m = types.InlineKeyboardMarkup(row_width=1)
    for tariff in tariffs:
        m.add(types.InlineKeyboardButton(text=tariff[0], callback_data=tariff[1]))
    return m
async def tariffs_key():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(*[types.KeyboardButton(text= t[0]) for t in  await TariffsTable().search(all=True)])
    return m
# def send_check(lang):
#     m = types.InlineKeyboardMarkup(row_width=1)
#
#     return m