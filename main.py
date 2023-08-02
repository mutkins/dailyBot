import logging
from aiogram.utils import executor
from create_bot import dp
import asyncio
from handlers import common, trello_cards_create_update, trello_user_settings, trello_cards_read
from notificator import scheduler

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


# Register handlers from handlers folder
common.register_handlers(dp)
trello_cards_create_update.register_handlers(dp)
trello_cards_read.register_handlers(dp)
trello_user_settings.register_handlers(dp)


async def on_startup(_):
    asyncio.create_task(scheduler.scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
