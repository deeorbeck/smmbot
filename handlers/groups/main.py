from aiogram import types
from loader import dp
from data import config
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],content_types=types.ContentType.ANY, state='*')
async def group_handler(message: types.Message):
    if message.reply_to_message:
        if message.reply_to_message.forward_from:
            try:
                await dp.bot.copy_message(message.reply_to_message.forward_from.id,config.GROUP,message.message_id)
                await message.reply("Yuborildi")
            except:
                await message.reply("Bu user botni tark etgan")
        else:
            await message.reply("Bu user ma'lumotlarini yashirgan")
@dp.callback_query_handler(lambda c: c.data, chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], state='*')
async def group_handler(call: types.CallbackQuery):
    msg_id = call.message.message_id
    text = str(call.message.text).split('\n')
    fullname = text[1]
    id = text[0].split(':')[1]
    contact = f'ID:{id}\n<a href="tg://user?id={id}">{fullname}</a>'
    contact += f"\n\n<i>Javob: {call.data}</i>"
    try:
        await dp.bot.send_message(chat_id=id,text=call.data)
        await dp.bot.edit_message_text(chat_id=config.GROUP,message_id=msg_id,text=contact)
    except:
        await call.message.reply("Bu user botni tark etgan")

