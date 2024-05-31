import os
import asyncio
from aiogram import types
from loader import dp
from handlers.users import functions as funcs
from aiogram.dispatcher import FSMContext
from states.user import User
from data import config
from utils.db_api import database
from datetime import datetime as dt
from keyboards.default.all import menu_markup,  informations_key, cities
from .userpermissons import is_member_all_chats






@dp.message_handler(content_types=['text'], state=User.menu, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	chat_id = message.from_user.id
	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)


	user_sections = texts.user_sections()
	if message.text == user_sections[0]:# send_question
		if not await is_member_all_chats(_user_data):
			return
		await message.answer(texts.send_theme_of_pres(), reply_markup=cities([texts.orqaga()]))
		await User.create_pres.set()
	elif message.text == user_sections[1]:  # 📊 Make an Abstract
		if not await is_member_all_chats(_user_data):
			return
		await message.answer(texts.send_theme_of_abs(), reply_markup=cities([texts.orqaga()]))
		await User.create_abs.set()
	# await User.send_ticker.set()
	elif message.text == user_sections[-4]:#📊 Statistics
		users = await database.UsersTable().search(count=True)
		await message.answer(texts.count_users().format(users))
		# await User.send_ticker.set()
	elif message.text == user_sections[-3]: #💸Пополнение баланса
		user = await database.UsersTable().search(chat_id=chat_id)
		balance = int(user[2])
		m = types.InlineKeyboardMarkup(row_width=1)
		m.add(types.InlineKeyboardButton(text=texts.take_payment(), callback_data='payment'))
		await message.answer(texts.fill_balance().format(balance), reply_markup=m)
		await User.payment.set()
	elif message.text == user_sections[-2]: #lang
		await message.answer(message.text, reply_markup=cities(config.langs.keys()))
		await User.lang.set()
	elif message.text == user_sections[-1]: #contact
		await message.answer(texts.contact())










@dp.message_handler(content_types=['text'], state=User.premium, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	id = message.from_user.id
	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)
	premium_sections = texts.premium_sections()
	if message.text == texts.main():
		await message.answer(texts.choose(), reply_markup=menu_markup(lang))
		await User.menu.set()
		return

	elif message.text == premium_sections[0]:
		count = (await database.UsersTable().search(reffer_by=id))[0]
		await message.answer(texts.your_refferal_link().format(count))
		await message.answer(texts.refferal_link().format(f"{(await dp.bot.get_me())['username']}?start={id}"), disable_web_page_preview=True)


