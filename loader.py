from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
import os
import json

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
# ishalal = open(os.path.join(BASE_DIR, 'newbase.json'), encoding='utf-8-sig')
# ishalal = json.load(ishalal)
# data_ishalal = {}
# for ish in ishalal:
#     data_ishalal[ish["Ticker"]] = ish["Compliance"]
#
# database = open(os.path.join(BASE_DIR, 'database.json'))
# database = json.load(database)
#
# tickers = []
# names = []
# for t in database:
#     if 'Ticker' in t.keys():
#         tickers.append(t['Ticker'].strip())
#     else:
#         tickers.append(0)
#     if 'Company' in t.keys():
#         name = t['Company'].split('-')[-1]
#         names.append(name.strip())
#     else:
#         names.append(0)