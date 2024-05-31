import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from .functions import checkMember
from aiogram.dispatcher import FSMContext
from states.user import User
from data import config
from utils.db_api import database
from datetime import datetime as dt, timedelta
from handlers.users.userpermissons import  is_member_all_chats
from keyboards.default.all import menu_markup,  informations_key, cities






@dp.message_handler(commands=['admin'], state='*',chat_type=types.ChatType.PRIVATE, chat_id=config.ADMINS)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = 'uz'
    if 'lang' in _user_data.keys():
        lang = _user_data['lang']
    await state.update_data(lang=lang)
    texts = config.Texts(lang)
    await message.answer("Admin panel", reply_markup=cities(texts.admin_sections()))
    await User.admin.set()




@dp.message_handler(CommandStart(), state='*',chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    _user_data['chat_id'] = id
    await state.update_data(_user_data)
    command_args = message.get_args()
    if command_args == 'survey':
        await dp.bot.forward_message(chat_id=id, from_chat_id=-1001596191086, message_id=732)
        await dp.bot.forward_message(chat_id=id, from_chat_id=-1001596191086, message_id=733)
        await message.answer("Yuqoridagilarni belgilaganingizdan so'ng loyihamiz haqida qo'shimcha fikrlaringizni yozib qoldiring👇", reply_markup=cities(["Fikr bildirmayman hammasi yaxshi😎"]))
        await User.survey.set()
        return
        # await message.answer()
    # if command_args and int(command_args) != int(id):
    #     _user_data['reffer_by'] = command_args
    db = database.UsersTable()
    user = await db.search(chat_id=id)

    if user:
        if not 'lang' in _user_data.keys():
            lang = user[1]
            _user_data['lang'] = lang
            await User.lang.set()

        await state.update_data(_user_data)
        # if not await is_member_all_chats(_user_data) or not await is_granted(_user_data):
        #     return
        await message.answer(config.Texts(lang=_user_data['lang']).choose(), reply_markup=menu_markup(_user_data['lang']))
        await User.menu.set()
        return
    await state.update_data(_user_data)
    await message.answer(f"<b>Til tanlang👇\nChoose a language👇\nВыберите язык👇</b>", reply_markup= cities(list(config.langs.keys())))
    await User.lang.set()
@dp.callback_query_handler(lambda c: c.data, state=User.confirm_joined)
async def poc_callback_but(call: types.CallbackQuery,  state: FSMContext):
    _user_data = await state.get_data()
    c = call.data
    if c == "followed":
        await call.message.delete()
        # if not await is_member_all_chats(_user_data):
        #     return
        await call.message.answer(config.Texts(lang=_user_data['lang']).choose(), reply_markup=menu_markup(_user_data['lang']))
        await User.menu.set()

@dp.message_handler(content_types=['text'], state=User.lang, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    if message.text in config.langs.keys():
        lang = config.langs[message.text]
        await state.update_data(lang=lang)
        users = database.UsersTable()
        if await users.search(id):
            await users.adduser(chat_id=id, lang=lang)
            await message.answer(config.Texts(lang=lang).choose(), reply_markup=menu_markup(lang))
            await User.menu.set()
            return
        reffer_by = 0
        if 'reffer_by' in _user_data.keys():
            reffer_by = _user_data['reffer_by']
            reffer_by_user = await users.search(chat_id=int(reffer_by))
            if reffer_by_user:
                lang_refferer = reffer_by_user[1]
                await dp.bot.send_message(chat_id=reffer_by, text=config.Texts(lang_refferer).refferal_successful_text().format(message.from_user.full_name, config.sums_per_reffer))
                # count_users_reffered = await users.search(reffer_by=reffer_by)
                await database.UsersTable().adduser(reffer_by, access=int(reffer_by_user[2]) + config.sums_per_reffer)
                # if count_users_reffered[0] + 1 in config.refferals.keys():
                #     old_access_time = reffer_by_user[2]
                #     old_access_time = dt.strptime(old_access_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
                #     next_date = old_access_time + timedelta(days=int(config.refferals[count_users_reffered[0] + 1] * 30))
                #     await database.UsersTable().adduser(reffer_by, access=next_date)
                #     await dp.bot.send_message(chat_id=reffer_by,text=config.Texts(lang_refferer).changed_access_time_via_refferal().format(count_users_reffered[0] + 1,next_date.strftime("%d.%m.%Y")))

        # next_day = dt.today() + timedelta(days=int(config.free_days))
        # formatted_date_string = next_day.strftime("%d.%m.%Y")
        await users.adduser(chat_id=id, lang=lang, access=config.default_sums, reffer_by=int(reffer_by))
        await message.answer(config.Texts(lang=lang).completly_started().format(config.default_sums))
        await message.answer(config.Texts(lang=lang).choose(), reply_markup=menu_markup(lang))
        await User.menu.set()
