import asyncio

from loader import bot,dp
from aiogram import types
from data import config
from utils.db_api import database
from aiogram.dispatcher import FSMContext
from states.user import User
from keyboards.default.all import admin_menu_key, tariffs_key
from datetime import datetime as dt, timedelta
from handlers.users import functions as funcs





@dp.message_handler(chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state=User.admin, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    sections = texts.admin_sections()
    if message.text == sections[0]:
        await message.answer("Foydalanuvchi idsini yuboring:")
        await User.enter_client_id.set()
    elif message.text == sections[6]: # channels
        db = database.ChannelsTable()
        channels = await db.search(all=True)
        markup = types.InlineKeyboardMarkup(row_width=2)
        for ch in channels:
            ch = ch[0]
            channel = await dp.bot.get_chat(ch)
            markup.add(
                types.InlineKeyboardButton(text=channel.full_name, url=channel.invite_link),
                types.InlineKeyboardButton(text="➖", callback_data=f"{ch}")
            )
        markup.add(types.InlineKeyboardButton(text="➕", callback_data="add"))
        markup.add(types.InlineKeyboardButton(text=texts.orqaga(), callback_data="back"))
        ###
        msg = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
        await dp.bot.delete_message(id, message_id=msg.message_id)
        ###
        await message.answer(message.text, reply_markup=markup)
        await User.admin_channels.set()
    elif message.text == sections[1]:
        m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        m.add(types.KeyboardButton(text=texts.orqaga()))
        await message.answer(texts.send_post_to_rek(), reply_markup=m)
        await User.sendtousers.set()
    elif message.text == sections[2]:# statistics
        db = database.UsersTable()
        users = await db.search(all=True)
        txt = texts.count_users()
        await funcs.db_to_excel(id, txt.format(len(users)))
    elif message.text == sections[3]:
        await message.answer(text=message.text, reply_markup=await tariffs_key())
        await User.get_tokens.set()
    elif message.text == sections[4]:
        await message.answer(text=message.text, reply_markup=await tariffs_key())
        await User.enter_tariff.set()
    elif message.text == sections[5]: # remove user
        await message.answer(texts.send_user_id(),
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(text=texts.orqaga())))
        await User.remove_user.set()
@dp.message_handler(chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state=User.enter_client_id, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer("Summa:")
    await User.add_sums.set()


@dp.callback_query_handler(lambda c: c.data, state=User.admin_channels, chat_type=types.ChatType.PRIVATE, chat_id=config.ADMINS)
async def poc_callback_but(call: types.CallbackQuery,  state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    c = call.data
    if c == "back":
        _user_data = await state.get_data()
        txt = "Admin panel"
        await call.message.answer(txt, reply_markup=await admin_menu_key(lang))
        await User.admin.set()
    elif c == "add":
        await call.message.answer(texts.enterchannel_id())
        await User.addchannel.set()
    else:
        db = database.ChannelsTable()
        await db.delete(c)
        await call.message.answer(texts.deletechannel().format(c), reply_markup=await admin_menu_key(lang))
        await User.admin.set()
    await call.message.delete()

@dp.message_handler(content_types='text', chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state=User.addchannel)
async def func(message: types.Message,  state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    try:
        channel_id = message.text
        chat = await dp.bot.get_chat(channel_id)
        db = database.ChannelsTable()
        await db.addchannel(channel_id)
        await message.answer(texts.appendchannel().format(chat.full_name))
        await message.answer("Admin panel", reply_markup=await admin_menu_key(lang))
        await User.admin.set()
    except:
        await message.answer(texts.promoteadminbot())

@dp.message_handler(content_types='text', chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state=User.get_tokens)
async def func(message: types.Message):
    tariff =await database.TariffsTable().search(title=message.text)
    await message.answer(await funcs.list_tokens(tariff[1]))
@dp.message_handler(content_types='text', chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state=User.enter_tariff)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    tariff =await database.TariffsTable().search(title=message.text)
    days = tariff[1]
    await state.update_data(days=days)
    await message.answer(f"{texts.enter_tokens_count()}👇\n /10 /20 /50",
                         reply_markup=types.ReplyKeyboardRemove())
    await User.enter_count.set()
@dp.message_handler(chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.enter_count, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    count = message.text.replace("/", '')
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    days = _user_data['days']
    if not count.isdigit():
        await message.answer(texts.enter_true_count())
        return
    count = int(count)
    for i in range(count):
        token = await funcs.generate_token()
        await database.TokensTable().add(token=token, days=days)
    await message.answer(await funcs.list_tokens(days), reply_markup=await admin_menu_key(lang))
    await User.admin.set()
@dp.message_handler(chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.remove_user, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    user_id = message.text.strip()
    if user_id == texts.orqaga():
        await message.answer(texts.admin_panel_text(), reply_markup=await admin_menu_key(lang))
        await User.admin.set()
        return
    db = database.UsersTable()
    user = await db.search(chat_id=user_id)
    if not user:
        await message.answer(texts.not_founded_user_text())
        return
    await db.adduser(user_id, access='2024-01-01 01:01:01')
    await message.answer(texts.user_deleted_successfully(), reply_markup=await admin_menu_key(lang))
    await User.admin.set()





@dp.message_handler(content_types=types.ContentType.ANY, chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state=User.sendtousers)
async def func(message: types.Message,  state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    if message.text == texts.orqaga():
        txt = texts.admin_panel_text()
        await message.answer(txt, reply_markup=await admin_menu_key(lang))
        await User.admin.set()
        return False
    db = database.UsersTable()
    users = await db.search(all=True)
    count = 0
    for u in users:
        chat_id = u[0]
        try:
            await dp.bot.forward_message(chat_id=chat_id, from_chat_id=id,message_id=message.message_id)
            count += 1
            await asyncio.sleep(1)
        except:
            pass
    txt = texts.sent_users_count()
    await message.answer(txt.format(count), reply_markup=await admin_menu_key(lang))
    await User.admin.set()
    # await User.wait.set()




# Tariff

@dp.callback_query_handler(lambda c: c.data, state=User.manage_tariff)
async def poc_callback_but(call: types.CallbackQuery,  state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    c = call.data
    if c == "back":
        _user_data = await state.get_data()
        txt = "Admin panel"
        await call.message.answer(txt, reply_markup=await admin_menu_key(lang))
        await User.admin.set()
    elif c == "add":
        await call.message.answer(texts.enter_tariff_name())
        await User.addtariff.set()
    elif c[0] == "i":
        days = c[1:]
        tariff = await database.TariffsTable().search(days=days)
        txt = texts.tariff_name_price()
        await call.message.answer(txt.format(tariff[0], tariff[1], tariff[2]))
    else:
        tariff = database.TariffsTable()
        await tariff.delete(days=c)
        await call.message.answer(texts.user_deleted_successfully(), reply_markup=await admin_menu_key(lang))
        await User.admin.set()
    await call.message.delete()

@dp.message_handler(content_types='text', chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE,
                    state=User.addtariff)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    title = message.text
    await state.update_data(title=title)
    await message.answer(texts.enter_days_count(), reply_markup=types.ReplyKeyboardRemove())
    await User.addtariffdays.set()

@dp.message_handler(content_types='text', chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE,
                    state=User.addtariffdays)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    days = message.text
    if not days.isdigit():
        await message.answer(texts.enter_only_numbers())
        return
    await state.update_data(days=days)
    await message.answer(texts.enter_tariff_price())
    await User.addtariffprice.set()
@dp.message_handler(content_types='text', chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE,
                    state=User.addtariffprice)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    price = message.text
    if not price.isdigit():
        await message.answer(texts.enter_tariff_price())
        return
    await state.update_data(price=price)
    _user_data = await state.get_data()
    tariff = database.TariffsTable()
    await tariff.add(_user_data['title'], _user_data['days'], _user_data['price'])
    await message.answer(texts.appended_tariff_text().format(_user_data["title"]), reply_markup=await admin_menu_key(lang))
    await User.admin.set()

@dp.callback_query_handler(lambda c: c.data, state='*', chat_id=config.ADMINS)
async def poc_callback_but(call: types.CallbackQuery,  state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    c = call.data
    if c[0] == "a":
        user_id = c.split()[-1]
        await state.update_data(user_id=user_id)
        await call.message.answer("Qo'shmoqchi bo'lgan summangizni yozing: ")
        await User.add_sums.set()
    if c.split()[0] == 'ignore':
        chat_id = c.split()[1]
        await dp.bot.send_message(chat_id=chat_id, text=texts.ignore_payment_check())

@dp.message_handler(content_types='text', chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.add_sums)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    user_id = _user_data['user_id']
    sums = int(message.text)

    if sums < 1000:
        await message.answer("1000?")
        return
    db = database.UsersTable()
    balance = int((await db.search(user_id))[2])
    balance += sums
    await db.adduser(chat_id=user_id, access=balance)
    await message.answer(f"{user_id}'s balance is {balance}!")
    await dp.bot.send_message(chat_id=user_id, text=texts.admin_confirmed().format(balance))


