import json

import requests
from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, performance, cabinet, end_test, \
    choice_language, choice_language_ru, cabinet_ru, performance_ru, choice_language_en, performance_en, cabinet_en


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [performance],
            [choice_language]
        ]
    elif tg_user['language'] == 'en':
        design = [
            [performance_en],
            [choice_language_en]
        ]
    else:
        design = [
            [performance_ru],
            [choice_language_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button():
    design = [[back_main_menu]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)