import json
import random

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from bot.buttons.inline_buttons import category_button, test_button
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import performance, end_test, performance_ru, performance_en
from bot.dispatcher import dp


async def get_test(category_id: str, words: list):
    category = json.loads(requests.get(url=f"http://127.0.0.1:8002/api/categories/detail/{category_id}").content)
    used_words = set(words)
    while True:
        num = random.randint(0, category['words_count'] - 1)
        word_id = category['words'][num]['id']
        if word_id not in used_words:
            break
    word = category['words'][num]
    word = json.loads(requests.get(url=f"http://127.0.0.1:8002/api/words/detail/{word['id']}").content)
    return word, category


@dp.message_handler(Text(equals=[performance, performance_ru, performance_en]))
async def test_performance_function(msg: types.Message, state: FSMContext):
    await state.set_state('choice_category')
    if msg.text == performance:
        await msg.answer(text="Kategoriyani tanlang 👇", reply_markup=await category_button(lang='uz'))
    elif msg.text == performance_en:
        await msg.answer(text="Select a category 👇", reply_markup=await category_button(lang='en'))
    else:
        await msg.answer(text="Выберите категорию 👇", reply_markup=await category_button(lang='ru'))
    message = await msg.answer(text="Lets go!", reply_markup=ReplyKeyboardRemove())
    await message.delete()


@dp.callback_query_handler(state='choice_category')
async def test_performance_function_2(call: types.CallbackQuery, state: FSMContext):
    word, category = await get_test(call.data, words=[])
    async with state.proxy() as data:
        data['words_count'] = category['words_count']
        data['word_number'] = 1
        data['words'] = [word['word']['id']]
        data['correct_answers'] = 0
        data['correct_answer'] = word['word']['name']
        data['category_id'] = category['id']
    await call.message.delete()
    await call.message.answer_photo(photo=open(word['word']['image'][22:], 'rb'),
                                    caption=f"Test 1\n\nFind the name of this {str.lower(category['name'])} 👆",
                                    reply_markup=await test_button(words=word))
    await state.set_state('test_performance')


@dp.callback_query_handler(Text(end_test), state="test_performance")
async def test_performance_function_3(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.delete()
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8002/api/telegram-users/chat_id/{call.from_user.id}/").content)
        if tg_user['language'] == 'uz':
            await call.message.answer(
                text=f"Siz testni yakunladingiz 🎉\n\nSiz to'plagan ball: {data['correct_answers'] / (data['word_number'] - 1) * 100}",
                reply_markup=await main_menu_buttons(call.from_user.id))
        elif tg_user['language'] == 'ru':
            await call.message.answer(
                text=f"Вы прошли тест 🎉\n\nВаша оценка: {data['correct_answers'] / (data['word_number'] - 1) * 100}",
                reply_markup=await main_menu_buttons(call.from_user.id)
            )
        else:
            await call.message.answer(
                text=f"You have completed the test 🎉\n\nYour score is: {data['correct_answers'] / (data['word_number'] - 1) * 100}",
                reply_markup=await main_menu_buttons(call.from_user.id)
            )
        await state.finish()


@dp.callback_query_handler(state="test_performance")
async def test_performance_function_4(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == data['correct_answer']:
            data['correct_answers'] = data['correct_answers'] + 1
        if data['word_number'] == data['words_count']:
            await call.message.delete()
            tg_user = json.loads(
                requests.get(url=f"http://127.0.0.1:8002/api/telegram-users/chat_id/{call.from_user.id}/").content)
            if tg_user['language'] == 'uz':
                await call.message.answer(
                    text=f"Siz barcha testni tugatdingiz 🎉\n\nSiz to'plagan ball: {data['correct_answers'] / data['words_count'] * 100}",
                    reply_markup=await main_menu_buttons(call.from_user.id))
            elif tg_user['language'] == 'ru':
                await call.message.answer(
                    text=f"Вы прошли весь тест 🎉\n\nВаша оценка: {data['correct_answers'] / data['words_count'] * 100}",
                    reply_markup=await main_menu_buttons(call.from_user.id)
                )
            else:
                await call.message.answer(
                    text=f"You have completed all tests 🎉\n\nYour score is: {data['correct_answers'] / data['words_count'] * 100}",
                    reply_markup=await main_menu_buttons(call.from_user.id)
                )
            await state.finish()
        else:
            word, category = await get_test(category_id=data['category_id'], words=data['words'])
            data['word_number'] = data['word_number'] + 1
            data['words'].append(word['word']['id'])
            data['correct_answer'] = word['word']['name']
            await call.message.delete()
            await call.message.answer_photo(photo=open(word['word']['image'][22:], 'rb'),
                                            caption=f"Test {data['word_number']}\n\nFind the name of this {str.lower(category['name'])} 👆",
                                            reply_markup=await test_button(words=word))
