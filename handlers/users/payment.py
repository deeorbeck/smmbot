from aiogram import types
from data import config
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
# from .functions import getData
# from .userpermissons import is_member_all_chats
from states.user import User
from aiogram.dispatcher import FSMContext
from keyboards.inline.all import getTariffs
from keyboards.default.all import cities, menu_markup
from utils.db_api import database
from datetime import datetime as dt, timedelta

# @dp.callback_query_handler(lambda c: c.data, state=User.choose_tariff)
# async def poc_callback_but(call: types.CallbackQuery,  state: FSMContext):
#     _user_data = await state.get_data()
#     lang = _user_data['lang']
#     texts = config.Texts(lang)
#     c = call.data
#     tariff = await database.TariffsTable().search(days=c)
#     if tariff:
#         await state.update_data(tariff=c)
#         await call.message.answer(texts.tariff_info().format(tariff[0], tariff[2]) , reply_markup=cities([texts.enter_token_text()]))
#         await User.enter_token.set()
#     await call.message.delete()
#
#
# @dp.message_handler(content_types=['text'], state=User.enter_token)
# async def func(message:types.Message,  state: FSMContext):
#     _user_data = await state.get_data()
#     lang = _user_data['lang']
#     texts = config.Texts(lang)
#     chat_id = message.from_user.id
#     token = message.text
#     if token == texts.enter_token_text():
#         await message.answer(texts.enter_token_by_admin(), reply_markup=cities([texts.orqaga()]))
#         return
#     elif token == texts.orqaga():
#         await User.choose_tariff.set()
#         txt = "\n".join(
#             [f"{tariff[0]} - {tariff[2]} so'm" for tariff in await database.TariffsTable().search(all=True)])
#         await dp.bot.send_message(chat_id=chat_id,
#                                   text=texts.choose_tariff_to_using().format(config.admin_username) + txt,
#                                   reply_markup=await getTariffs())
#         return
#
#     data = await database.TokensTable().search(token=token)
#     if not data:
#         await message.answer(texts.ignore_token_text())
#         return
#     token, days = data
#     await database.TokensTable().delete(token)
#     next_date = dt.today() + timedelta(days=int(days))
#     await database.UsersTable().adduser(chat_id=chat_id, access=next_date)
#     await dp.bot.send_message(chat_id=chat_id,
#                               text=texts.changed_access_time().format(next_date.day, next_date.month, next_date.year))
#
#     txt = f'✅  <b><a href="tg://user?id={chat_id}">{message.from_user.full_name}</a> ({chat_id})</b> subscribed via <code>{token}</code> '
#     for a in config.ADMINS:
#         try:
#             await dp.bot.send_message(chat_id=a, text=txt)
#         except:
#             pass
@dp.callback_query_handler(lambda c: c.data, state=User.payment)
async def func(call: types.CallbackQuery, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    if call.data == 'payment':
        await call.message.delete()
        await call.message.answer(texts.send_check(), reply_markup=types.ReplyKeyboardRemove())
        await User.send_bill_check.set()


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=User.send_bill_check, content_types=['photo', 'document'])
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    admin_markup = types.InlineKeyboardMarkup(row_width=1)
    admin_markup.add(types.InlineKeyboardButton(text="Qo'shish", callback_data=f"a {message.from_user.id}"))
    admin_markup.add(types.InlineKeyboardButton(text="Chek xato", callback_data=f"ignore {message.from_user.id}"))
    for a in config.ADMINS:
        if not int(a):
            continue
        await dp.bot.forward_message(chat_id=a, from_chat_id=message.from_user.id, message_id=message.message_id)
        db = database.UsersTable()
        user = await db.search(chat_id=message.from_user.id)
        txt = f"<b>ID:</b> {message.from_user.id}\n"
        txt += f"<b>Ism:</b> {message.from_user.full_name}\n"
        txt += f"<b>Hisobi:</b> {user[2]} so'm\n\n"

        await dp.bot.send_message(chat_id=a, text=txt, reply_markup=admin_markup)
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=texts.wait_confirm().format(config.admin_username))
    await User.payment.set()


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=User.send_bill_check, content_types=types.ContentTypes.ANY)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    await message.answer(texts.send_only_photo())