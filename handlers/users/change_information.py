from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from .functions import checkMember, check_number
from aiogram.dispatcher import FSMContext
from states.user import User
from data import config
from keyboards.default.all import menu_markup, cities as ci
from utils.db_api import api_client
from keyboards.inline.all import inline_template
from utils.db_api.database import DataBaseSql
import handlers.users.functions as funcs



@dp.message_handler(content_types=['text'],chat_type=types.ChatType.PRIVATE, state=User.change_information)
async def func(message: types.Message, state: FSMContext):
    section = message.text
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    informations_section = await texts.information_sections()
    informations = await texts.informations()
    if section == informations_section[-1]:
        await message.answer(await texts.sections_text(), reply_markup=await menu_markup(lang))
        await User.menu.set()
    elif section == informations_section[0]:
        await message.answer(await texts.change_buttons(),
                             reply_markup=await ci(informations))
    elif section == informations[0]:
        await message.answer(await texts.enter_name(),
                             reply_markup=await ci(informations))
        await User.change_name.set()
    elif section == informations[1]:
        await message.answer(await texts.phone_number(),
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                 types.KeyboardButton(text=await texts.phone_number_button(), request_contact=True)))
        await User.change_phone.set()
    elif section == informations[2]:
        cities = await funcs.get_cities(lang)
        data = [{"text": c['name'], "data": f'{c["id"]} {c["name"]}'} for c in cities]
        data.append({'text': await texts.orqaga(), "data": await texts.orqaga()})
        m = await inline_template(data, row_width=1)
        await message.answer(await texts.select_city(), reply_markup=m)
        await User.change_city.set()
    elif section == informations[3]:
        await message.answer("Tilni tanlang👇\nВыберите язык👇", reply_markup=await ci(config.langs.keys()))
        await User.lang.set()
    elif section == informations[4]:
        await message.answer(section, reply_markup=await menu_markup(lang))
        await User.menu.set()
@dp.callback_query_handler(lambda c : c.data, chat_type=types.ChatType.PRIVATE, state=User.change_city)
async def func(call: types.CallbackQuery, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    if call.data == await texts.orqaga():
        await call.message.answer(await texts.change_buttons(),
                             reply_markup=await ci(await texts.informations()))
        await User.change_information.set()
        await call.message.delete()
        return
    chat_id = call.from_user.id
    city = str(call.data).split()
    city_id = city.pop(0)
    city_name = " ".join(city)

    await state.update_data(city_id=city_id, city_name=city_name)
    # print(city_id, city_name)
    _user_data = await state.get_data()
    db = DataBaseSql()
    await db.adduser(chat_id=chat_id,  city_only=True, city_id=city_id, city_name=city_name)
    await call.message.delete()
    await call.message.answer(await texts.changed_successfully(), reply_markup=await menu_markup(lang))
    await User.menu.set()
@dp.message_handler(content_types=['contact'],chat_type=types.ChatType.PRIVATE, state=User.change_phone)
async def func(message: types.Message, state: FSMContext):
    id = message.from_user.id
    db = DataBaseSql()
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    contact = message.contact
    await state.update_data(phone=str(contact.phone_number).replace("+", ''),chat_id=contact.user_id)
    await db.adduser(chat_id=id, phone_only=str(contact.phone_number).replace("+", ''))
    await message.answer(await texts.changed_successfully(), reply_markup=await menu_markup(lang))
    await User.menu.set()
@dp.message_handler(content_types=types.ContentTypes.ANY,chat_type=types.ChatType.PRIVATE, state=User.change_phone)
async def func(message: types.Message, state: FSMContext):
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    await message.answer(await texts.only_tg_number(),
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).
                         add(types.KeyboardButton(text=await texts.phone_number_button(), request_contact=True)))

@dp.message_handler(content_types=['text'],chat_type=types.ChatType.PRIVATE, state=User.change_name)
async def func(message: types.Message, state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    lang = _user_data['lang']
    texts = config.Texts(lang)
    full_name = message.text
    await state.update_data(full_name=full_name)
    db = DataBaseSql()
    await db.adduser(chat_id=id, name_only=full_name)
    await message.answer(await texts.changed_successfully(), reply_markup=await menu_markup(lang))
    await User.menu.set()
