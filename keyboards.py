from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton
import datetime
from common_tools import get_month_days, get_month_name, get_year


def get_additional_props():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('/срок')
    kb.add(button)
    button = KeyboardButton('/описание')
    kb.add(button)
    button = KeyboardButton('/сохранить')
    kb.add(button)
    return kb


def get_date_widget(iterator=0):
    ikb = InlineKeyboardMarkup(row_width=7)
    buttons = []
    month_days = get_month_days(iterator=iterator)
    prev_butt = InlineKeyboardButton(text='<<', callback_data='previous')
    month_butt = InlineKeyboardButton(text=f'{get_month_name(iterator=iterator)} {get_year(iterator=iterator)}', callback_data='nothing')
    next_butt = InlineKeyboardButton(text='>>', callback_data='next')
    ikb.add(prev_butt, month_butt, next_butt)
    for day in month_days:
        button = InlineKeyboardButton(text=day[2], callback_data=f'{day[0]}-{day[1]}-{day[2]}')
        buttons.append(button)
    ikb.add(*buttons)
    return ikb

#
#
# def get_another_one_kb():
#     kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button = KeyboardButton('/еще_вариант')
#     kb.add(button)
#     button = KeyboardButton('/сохранить_рецепт')
#     kb.add(button)
#     button = KeyboardButton('/ок')
#     kb.add(button)
#     return kb
#
#
# def get_welcome_kb():
#     kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button = KeyboardButton('/каталог')
#     kb.add(button)
#     button = KeyboardButton('/мои_рецепты')
#     kb.add(button)
#     return kb
#
#
# def saved_recipes_actions():
#     kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button = KeyboardButton('/удалить_всё')
#     kb.add(button)
#     button = KeyboardButton('/удалить_один')
#     kb.add(button)
#     return kb
#
#
# def saved_recipes_list(user_id):
#     kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     saved_recipes = classes.RecipesDB.get_saved_recipes_list_by_user_id(user_id)
#     for saved_recipe in saved_recipes:
#         button = KeyboardButton(saved_recipe.recipe_title)
#         kb.add(button)
#     return kb
