import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu, choice_language, choice_language_ru, back_main_menu_ru, back_main_menu_en, \
    choice_language_en
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_en]), )
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_en]), )
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8002/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    try:
        if tg_user['detail']:
            await state.set_state('language_1')
            await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык

-------------

Select a language""", reply_markup=await language_buttons())
    except KeyError:
        if tg_user.get('language') == 'uz':
            await msg.answer(text=f"Bot yangilandi ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        elif tg_user['language'] == 'en':
            await msg.answer(text="The bot has been updated ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def language_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    for admin in admins:
        await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={call.from_user.id}'>{call.from_user.id}</a>
Username: @{call.from_user.username}
Ism-Familiya: {call.from_user.full_name}""", parse_mode='HTML')
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        'language': call.data.split('_')[-1]
    }
    requests.post(url=f"http://127.0.0.1:8002/api/telegram-users/create/", data=data)
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Hush kelibsiz 😊", reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == 'en':
        await call.message.answer(text="Welcome 😊", reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Добро пожаловать 😊", reply_markup=await main_menu_buttons(call.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru, choice_language_en]))
async def change_language_function_1(msg: types.Message):
    await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык

-------------

Select a language""", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'))
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8002/api/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    s = requests.put(url=f"http://127.0.0.1:8002/api/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == 'en':
        await call.message.answer(text="The language has been changed 🇺🇿",
                                  reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))
