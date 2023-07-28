from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.TrelloCardFSM import TrelloCardFSM
import db.database
import keyboards
from handlers import common
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
    async with state.proxy() as data:
        data['card_title'] = message.text
        print('')
    await save_or_add_props(message=message, state=state)


async def save_or_add_props(message: types.Message, state: FSMContext):
    await TrelloCardFSM.save_or_add_props.set()
    await message.answer("Сохранить карточку или добавить описание / срок", reply_markup=keyboards.get_additional_props())


async def save_card(message: types.Message, state: FSMContext):
    log.debug(f"DEF save_card, message {message.text}")
    async with state.proxy() as data:
        user = db.database.get_user_by_chat_id(chat_id=message.from_user.id)
        try:
            cards.add_card(idList=user.get_todolist_id(), key=user.get_trello_key(), token=user.get_trello_token(),
                       name=data.get('card_title'), desc=data.get('card_desc'), due=data.get('card_due'))
        except Exception as e:
            await message.answer(e)
            raise e
    await message.answer("Карточка сохранена")
    await common.reset_state(state=state)


async def ask_card_due(message: types.Message, state: FSMContext):
    log.debug(f"DEF ask_card_due, message {message.text}")
    await message.answer("Введите срок задачи", reply_markup=keyboards.get_date_widget())
    await TrelloCardFSM.waiting_card_due.set()


async def set_card_due(call: types.CallbackQuery, state: FSMContext):
    log.debug(f"DEF set_card_due, callback {call.data}")
    async with state.proxy() as data:
        data['card_due'] = call.data
    await save_or_add_props(message=call.message, state=state)


async def ask_card_desc(message: types.Message, state: FSMContext):
    log.debug(f"DEF ask_card_desc, message {message.text}")
    await message.answer("Введите описание задачи")
    await TrelloCardFSM.waiting_card_desc.set()


async def set_card_desc(message: types.Message, state: FSMContext):
    log.debug(f"DEF set_card_desc, message {message.text}")
    async with state.proxy() as data:
        data['card_desc'] = message.text
    await save_or_add_props(message=message, state=state)


async def send_random_value(call: types.CallbackQuery):
    await call.answer(f'вы выбрали {call.message.text}')


async def next_month(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if not data.get('month_iterator'):
            data['month_iterator'] = 0
        data['month_iterator'] += 1
        await call.message.edit_text("Введите срок задачи", reply_markup=keyboards.get_date_widget(iterator=data.get('month_iterator')))


async def previous_month(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if not data.get('month_iterator'):
            data['month_iterator'] = 0
        data['month_iterator'] -= 1
        await call.message.edit_text("Введите срок задачи", reply_markup=keyboards.get_date_widget(iterator=data.get('month_iterator')))


def register_handlers(dp: Dispatcher):

    # T1 user sends /add_card to create new card
    dp.register_message_handler(ask_card_title, commands=['add_card'], state='*')
    # T1.1 user sends card title, save it, then send him a keybord with additional actions
    dp.register_message_handler(set_card_title, state=TrelloCardFSM.waiting_card_title)
    # T1.2 user sends /сохранить, set it and save card
    dp.register_message_handler(save_card, commands=['сохранить'], state=TrelloCardFSM.save_or_add_props)
    # T1.3 user sends /срок
    dp.register_message_handler(ask_card_due, commands=['срок'], state=TrelloCardFSM.save_or_add_props)
    # T1.4 user sends card's due, save it, then send him a keybord with additional actions
    # dp.register_message_handler(set_card_due, state=TrelloCardFSM.waiting_card_due)
    # T1.3 user sends /описание
    dp.register_message_handler(ask_card_desc, commands=['описание'], state=TrelloCardFSM.save_or_add_props)
    # T1.4 user sends card's due, save it, then send him a keybord with additional actions
    dp.register_message_handler(set_card_desc, state=TrelloCardFSM.waiting_card_desc)

    dp.register_callback_query_handler(next_month, text='next', state=TrelloCardFSM.waiting_card_due)
    dp.register_callback_query_handler(previous_month, text='previous', state=TrelloCardFSM.waiting_card_due)
    dp.register_callback_query_handler(set_card_due, state=TrelloCardFSM.waiting_card_due)

