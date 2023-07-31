from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
import common_tools
import Trello.cards
from handlers.TrelloCardFSM import TrelloCardFSM
import db.database
import keyboards
from handlers import common, trello_cards_read
import logging
from Trello import cards
from create_bot import dp


# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def ask_card_title(message: types.Message, state: FSMContext):
    # Reset state if it exists (if user is in the process)
    await common.reset_state(state=state)
    log.debug(f"DEF add_card, message {message.text}")
    await message.answer("Введите название задачи")
    await TrelloCardFSM.waiting_card_title.set()


async def set_card_title(message: types.Message, state: FSMContext):
    log.debug(f"DEF set_card_title, message {message.text}")
    try:
        await save_card(message=message, state=state, name=message.text,chat_id=message.from_user.id)
        await trello_cards_read.send_card_by_name(message=message, state=state, name=message.text, chat_id=message.from_user.id)
    except Exception as e:
        await message.answer(e)
        raise e
    await common.reset_state(state=state)


async def save_card(chat_id, message: types.Message, state: FSMContext, name=None, due=None, desc=None, card_id=None,
                    is_done=False):
    user = db.database.get_user_by_chat_id(chat_id=chat_id)
    idList = user.get_donelist_id() if is_done else user.get_todolist_id()
    try:
        cards.add_card(idList=idList, key=user.get_trello_key(), token=user.get_trello_token(),
                       name=name, due=due, desc=desc, card_id=card_id, is_done=is_done)
    except Exception as e:
        raise e


async def ask_card_due(call: types.CallbackQuery, state: FSMContext):
    # await call.message.answer("Введите срок задачи", reply_markup=keyboards.get_date_widget())
    await call.message.edit_text(call.message.text, reply_markup=keyboards.get_date_widget())
    await TrelloCardFSM.waiting_card_due.set()


async def set_card_due(call: types.CallbackQuery, state: FSMContext):
    card_id = common_tools.extract_card_id(call.message.text)
    await save_card(message=call.message, state=state, due=call.data, chat_id=call.from_user.id, card_id=card_id)
    await trello_cards_read.send_card_by_id(message=call.message, chat_id=call.from_user.id, card_id=card_id)
    await common.reset_state(state=state)


async def next_month(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if not data.get('month_iterator'):
            data['month_iterator'] = 0
        data['month_iterator'] += 1
        await call.message.edit_text(call.message.text, reply_markup=keyboards.get_date_widget(iterator=data.get('month_iterator')))


async def previous_month(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if not data.get('month_iterator'):
            data['month_iterator'] = 0
        data['month_iterator'] -= 1
        await call.message.edit_text(call.message.text, reply_markup=keyboards.get_date_widget(iterator=data.get('month_iterator')))


async def set_card_done(call: types.CallbackQuery, state: FSMContext):
    card_id = common_tools.extract_card_id(call.message.text)
    await save_card(message=call.message, state=state, chat_id=call.from_user.id, card_id=card_id, is_done=True)
    await call.answer("Так держать!")
    await call.message.delete()
    await common.reset_state(state=state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_card_title, commands=['add_card'], state='*')
    dp.register_message_handler(set_card_title, state=TrelloCardFSM.waiting_card_title)

    dp.register_callback_query_handler(ask_card_due, text='change_due', state='*')
    dp.register_callback_query_handler(set_card_due, state=TrelloCardFSM.waiting_card_due)

    dp.register_callback_query_handler(next_month, text='next', state=TrelloCardFSM.waiting_card_due)
    dp.register_callback_query_handler(previous_month, text='previous', state=TrelloCardFSM.waiting_card_due)

    dp.register_callback_query_handler(set_card_done, text='done', state='*')
