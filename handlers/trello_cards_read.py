from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import db.database
import keyboards
from handlers import common
import logging
from Trello import cards
from common_tools import get_hf_date_diff
from create_bot import bot

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def send_all_todo_cards(message: types.Message, state: FSMContext):
    # Reset state if it exists (if user is in the process)
    await common.reset_state(state=state)
    user = db.database.get_user_by_chat_id(chat_id=message.from_user.id)
    to_do_cards = cards.get_cards_in_list(idList=user.get_todolist_id(), key=user.get_trello_key(), token=user.get_trello_token())
    if not to_do_cards:
        await send_no_card_msg(chat_id=message.from_user.id)
    else:
        for card in to_do_cards:
            await send_card(card=card, chat_id=message.from_user.id)


async def send_card(card, chat_id):
    title = f"<b>{card.get('name')}</b>\n"
    desc = f"Описание: {card.get('desc')}\n" if card.get('desc') else ''
    due = f"Срок: <b>{get_hf_date_diff(card.get('due'))}</b>\n" if card.get('due') else ''
    id = f"<tg-spoiler>id:{card.get('id')}</tg-spoiler>"
    await bot.send_message(chat_id=chat_id, text=f"{title}{desc}{due}{id}", parse_mode="HTML",
                           reply_markup=keyboards.get_card_actions())


async def send_no_card_msg(chat_id):
    await bot.send_message(chat_id=chat_id, text=f"Задач нет", parse_mode="HTML")


async def send_card_by_name(name, message: types.Message, state: FSMContext, chat_id):
    user = db.database.get_user_by_chat_id(chat_id=chat_id)
    card = cards.get_card_by_name(idList=user.get_todolist_id(), key=user.get_trello_key(),
                                  token=user.get_trello_token(),name=name)
    await send_card(card=card, chat_id=chat_id)


async def send_card_by_id(message: types.Message, chat_id, card_id):
    user = db.database.get_user_by_chat_id(chat_id=chat_id)
    card = cards.get_card_by_id(key=user.get_trello_key(), token=user.get_trello_token(), id=card_id)
    await send_card(card=card, chat_id=chat_id)


def register_handlers(dp: Dispatcher):
    # TR1 user sends /cards
    dp.register_message_handler(send_all_todo_cards, commands=['cards'], state='*')
