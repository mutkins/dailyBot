from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from db import database


async def send_welcome(message: types.Message):
    await message.answer("<b>Секретарь поможет в планировании и исполнении ежедневных задач</b>\n", parse_mode="HTML")
    await check_if_trello_creds_exist(message=message)


async def check_if_trello_creds_exist(message: types.Message):
    if not database.get_user_by_chat_id(message.from_user.id):
        await message.answer("<b>Внимание: не установлены ключ и токен Trello. Для установки: /user</b>\n",
                             parse_mode="HTML")


async def send_help(message: types.Message):
    await message.answer("<b>Откуда взять токен и ключ трелло?</b>\n"
                         "1. Зарегистрироваться в Trello https://trello.com/signup\n"
                         "2. В настройках Trello создать Power-Ups, сгенерировать api-key и token "
                         "https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/",
                         parse_mode="HTML")
    await check_if_trello_creds_exist(message=message)


async def cancel_handler(message: types.Message, state: FSMContext):
    reset_state(state=state)
    # Cancel state and inform user about it
    await send_welcome(message)


async def reset_state(state: FSMContext):
    # Cancel state if it exists
    current_state = await state.get_state()
    if current_state:
        await state.finish()


def register_handlers(dp: Dispatcher):
    # A1 user sends /help or smthg like it
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel', 'отмена'])
    dp.register_message_handler(send_help, commands=['help'])


