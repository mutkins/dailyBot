import asyncio
import aioschedule
import configparser
from notificator import send_trello_card_exp
from db import database
config = configparser.ConfigParser()
config.read('settings.ini')



async def scheduler():
    # aioschedule.every().minute.do(send_trello_card_exp.send_notifications)
    aioschedule.every().hour.at(':00').do(send_trello_card_exp.send_notifications)
    # aioschedule.every(10).seconds.do(send_trello_card_exp.send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
