from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import ChatNotFound

from loader import dp
from states import GetMessage
from utils.db_api.db_commands import create_client


@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    await create_client(telegram_id=message.from_user.id,
                        username=message.from_user.username)
    deep_link = message.get_args()
    if deep_link == '':
        await message.answer('🎅 Хоу-хоу-хоу!\n\n'
                             '❤️‍🔥 И так, чтобы получать анонимные сообщения тебе надо <b>скопировать ссылку</b> ниже.\n'
                             '📎 Выложить ее в любой мессенджер, например, история в ВК, в Instagram или вовсе в личный канал в Telegram!\n'
                             '🎅 В дальнейшем остается лишь одно - ждать новых анонимных сообщений!\n\n'
                             f'📍 Твоя персональная ссылка: https://t.me/SecretDotBot?start={message.from_user.id}\n\n'
                             f'❤ Если не очень понятно, сейчас отправлю видео, где покажу это на примере️')
        await message.answer_video('BAACAgIAAxkBAAMIY6rxWllvTzYAAZApU20_liETFteEAAKbJAACCLdYSeh7cg0H0CZjLAQ')
    else:
        await message.answer('🎅 Хоу-хоу-хоу!\n'
                             '❤️‍🔥 Отправь мне свое анонимное пожелание, а я передам его адресату.\n\n'
                             '📍Пссс... Если тоже хочешь получать пожелания, введи комманду /start')
        await GetMessage.msg.set()

        state = dp.current_state(chat=message.chat.id)

        await state.update_data(
            {
                'chat_id': deep_link
            }
        )


@dp.message_handler(state=GetMessage.msg)
async def send_secret_message(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await state.reset_state(True)
        await start_cmd(message)
    else:
        try:
            data = await state.get_data()
            chat_id = data['chat_id']
            text = message.text
            await dp.bot.send_message(
                chat_id=chat_id,
                text='🎅 Тебе пришло новое пожелание!\n\n'
                     f'{text}'
            )
            await message.answer('🎅 Я успешно доставил сообщение до адресата!\n\n'
                                 '📍Пссс... Если тоже хочешь получать пожелания, введи комманду /start')
        except ChatNotFound:
            await message.answer('🎅 К сожалению, я не смог доставить твое пожелание..\n'
                                 'Такого человека я не знаю :(')

        await state.reset_state(True)
