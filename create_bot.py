import configparser
import logging
import os
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv

storage = MemoryStorage()
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.environ.get('tgBot_id'))
dp = Dispatcher(bot, storage=storage)
