from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import db.database
import keyboards
from handlers import common
import logging
from Trello import cards
from common_tools import get_hf_date_diff
from create_bot import dp
from handlers.TrelloCardFSM import TrelloCardFSM

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def get_all_todo_cards(message: types.Message, state: FSMContext):
    # Reset state if it exists (if user is in the process)
    await common.reset_state(state=state)
    user = db.database.get_user_by_chat_id(chat_id=message.from_user.id)
    to_do_cards = cards.get_cards_in_list(idList=user.get_todolist_id(), key=user.get_trello_key(), token=user.get_trello_token())
    for card in to_do_cards:
        await message.answer(f"<b>{card.get('name')}</b>\n{card.get('desc')}\nСРОК: {get_hf_date_diff(card.get('due'))}", parse_mode="HTML")






























def register_handlers(dp: Dispatcher):

    # TR1 user sends /cards
    dp.register_message_handler(get_all_todo_cards, commands=['cards'], state='*')
