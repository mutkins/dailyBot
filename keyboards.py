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


def get_card_actions():
    ikb = InlineKeyboardMarkup(row_width=2)
    change_due_butt = InlineKeyboardButton(text='Изменить срок', callback_data='change_due')
    done_button = InlineKeyboardButton(text='Сделано', callback_data='done')
    ikb.add(change_due_butt, done_button)
    return ikb


def get_notifications_switch(status):
    buttons = []
    ikb = InlineKeyboardMarkup(row_width=4)
    if status:
        button = InlineKeyboardButton(text='Выключить', callback_data='notification_off')
        ikb.add(button)
        for i in range(6, 14):
            button = InlineKeyboardButton(text=f'{i}:00', callback_data=f'{i}:00')
            buttons.append(button)
        ikb.add(*buttons)
    else:
        button = InlineKeyboardButton(text='Включить', callback_data='notification_on')
        ikb.add(button)
    return ikb
