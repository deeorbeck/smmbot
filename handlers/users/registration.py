from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from .functions import checkMember, check_number
from aiogram.dispatcher import FSMContext
from states.user import User
from data import config
from utils.db_api.database import DataBaseSql
from keyboards.default.all import menu_markup
from utils.db_api.api_client import register, confirm_password
from utils.db_api import api_client
import handlers.users.functions as funcs
from keyboards.inline.all import inline_template


@dp.message_handler(content_types=['contact'],chat_type=types.ChatType.PRIVATE, state=User.phone_number)
async def func(message: types.Message, state: FSMContext):
    db = DataBaseSql()
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    contact = message.contact
    phone= str(contact.phone_number).replace("+", '')
    if phone[:3] != "998":
        await message.answer((await texts.works_only_in_uz()).format(config.taxi))
    await state.update_data(phone=phone, first_name=contact.first_name, last_name=contact.last_name or " ", chat_id=contact.user_id)
    await message.answer(await texts.enter_name()
                         , reply_markup=types.ReplyKeyboardRemove())
    await User.first_name.set()

@dp.message_handler(content_types=types.ContentTypes.ANY,chat_type=types.ChatType.PRIVATE, state=User.phone_number)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    await message.answer(await texts.only_tg_number(),
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).
                         add(types.KeyboardButton(text=await texts.phone_number_button(), request_contact=True)))



@dp.message_handler(content_types=['text'],chat_type=types.ChatType.PRIVATE, state=User.first_name)
async def func(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    lang = (await state.get_data())['lang']
    cities = await funcs.get_cities(lang)
    data = [{"text": c['name'], "data": f'{c["id"]} {c["name"]}'} for c in cities]
    m = await inline_template(data, row_width=1)
    await message.answer(await config.Texts(lang).enter_city(), reply_markup=m)
    await User.enter_city.set()

@dp.callback_query_handler(lambda c : c.data, chat_type=types.ChatType.PRIVATE, state=User.enter_city)
async def func(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    city = str(call.data).split()
    city_id = city.pop(0)
    city_name = " ".join(city)
    lang = (await state.get_data())['lang']
    await state.update_data(city_id=city_id, city_name=city_name)
    _user_data = await state.get_data()
    db = DataBaseSql()
    if await db.search(chat_id=chat_id):
        await db.delete(chat_id=chat_id)
    db = DataBaseSql()
    await db.adduser(chat_id=chat_id, auth_key="null", msg_id=0, full_name=_user_data['full_name'],
                     phone_number=_user_data['phone'], gender=0, city_id=city_id, city_name=city_name)
    await call.message.delete()
    await call.message.answer(await config.Texts(lang).choose(), reply_markup=await menu_markup(lang))
    await User.menu.set()


