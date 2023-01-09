from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BotBlocked

from data.config import admins
from loader import dp
from states import GetMessage
from utils.db_api.db_commands import get_clients, get_clients_count


@dp.message_handler(Command('send'), user_id=admins[0])
async def send_to_clients(message: types.Message):
    await message.answer('Введите сообщение для рассылки')
    await GetMessage.mailing.set()


@dp.message_handler(state=GetMessage.mailing)
async def mailing_clients(message: types.Message, state: FSMContext):
    text = message.text
    clients = await get_clients()
    try:
        for client in clients:
            await dp.bot.send_message(
                chat_id=client,
                text=text
            )
    except BotBlocked:
        pass

    await message.answer('Рассылка завершена')
    await state.reset_state(True)


@dp.message_handler(Command('count'), user_id=admins[0])
async def get_count_clients(message: types.Message):
    count = await get_clients_count()
    await message.answer(f'В боте на данный момент насчитывается: {count}')
