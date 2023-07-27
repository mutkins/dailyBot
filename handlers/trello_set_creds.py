from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import keyboards
from handlers import common
import logging
from Trello import cards
import dotenv
import os
from db import database


# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class TrelloUserFSM(StatesGroup):
    waiting_trello_key = State()
    waiting_trello_token = State()


async def ask_trello_key(message: types.Message, state: FSMContext):
    # Reset state if it exists (if user is in the process)
    await common.reset_state(state=state)
    await message.answer("Введите ключ trello, он имеет вид 0d7ba3fa37aef1e955e182000aed3bc8")
    await TrelloUserFSM.waiting_trello_key.set()


async def set_trello_key(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['trello_key'] = message.text
    await ask_trello_token(message=message, state=state)


async def ask_trello_token(message: types.Message, state: FSMContext):
    await message.answer("Введите токен trello, он имеет вид ATTAb999b5a0254a0e00d2504aed7777777e10af51a95c66d19d95ef3e9b650dc414B53CFССС")
    await TrelloUserFSM.waiting_trello_token.set()


async def set_trello_token(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['trello_token'] = message.text
    await save_key_and_token(message=message, state=state)


async def save_key_and_token(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        newbie = database.Members(chat_id=message.from_user.id, trello_key=data['trello_key'],
                                  trello_token=data['trello_token'])
        newbie.add_member()
    await message.answer("Ключ и токен сохранены")
    await common.reset_state(state=state)


def register_handlers(dp: Dispatcher):
    # U1 user sends /user to reg trello key and token
    dp.register_message_handler(ask_trello_key, commands=['user'], state='*')
    # U2 user sends card title, save it, then ask token
    dp.register_message_handler(set_trello_key, state=TrelloUserFSM.waiting_trello_key)
    # U3 user sends card title, save it, then ask token
    dp.register_message_handler(set_trello_token, state=TrelloUserFSM.waiting_trello_token)
