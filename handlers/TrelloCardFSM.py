from aiogram.dispatcher.filters.state import State, StatesGroup


class TrelloCardFSM(StatesGroup):
    waiting_card_title = State()
    save_or_add_props = State()
    waiting_card_due = State()
    waiting_card_desc = State()