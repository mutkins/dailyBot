from db.database import get_users
from create_bot import bot
from Trello.cards import get_cards_in_list
from handlers.trello_cards_read import send_card
from operator import itemgetter
from datetime import datetime
from main import log


async def send_notifications():
    log.info("It's time to check notification to send")
    for user in get_users():
        log.info(f"User with chat_id={user.get_chat_id()}, check if his notice time equal with now")
        if user.get_notice_state() and user.get_notice_time()[0:2] == datetime.now().strftime('%H'):
            log.info(f"It's equal")
            await send(user=user)


async def send(user):
    log.info("It's time to check if some cards exist is user's list")
    cards_to_send = get_cards_in_list(idList=user.get_todolist_id(), key=user.get_trello_key(),
                              token=user.get_trello_token())
    log.info(f"cards_to_send={cards_to_send}")
    cards_to_send.sort(key=itemgetter('due'), reverse=True)
    for card in cards_to_send:
        log.info(f"Sending card {card.get('name')}")
        await send_card(card, chat_id=user.get_chat_id())
