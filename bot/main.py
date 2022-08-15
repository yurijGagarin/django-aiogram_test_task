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

from airtable.airtable_manager import create_user, UserAlreadyExist
from bot.config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
load_dotenv()


class Form(StatesGroup):
    username = State()
    password = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.username.set()

    await message.answer(f"Welcome <b>{message.from_user.first_name}</b>\nWrite desired username 👇")


@dp.message_handler(state='*', commands='restart')
@dp.message_handler(Text(equals='restart', ignore_case=True), state='*')
async def restart_handler(message: types.Message, state: FSMContext):
    await state.reset_state()

    await Form.username.set()
    await message.reply('Let`s try again.')


@dp.message_handler(state=Form.username)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

    await Form.password.set()
    await message.answer("Write desired password 👇")


@dp.message_handler(state=Form.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = str(message.text)
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Your credentials:'),
                md.text('Your login:', md.bold(data['username'])),
                md.text('Your password:', md.code(data['password'])),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        try:
            create_user(
                user_id=message.from_user.id,
                username=data['username'],
                password=data['password'],
                tg_username=message.from_user.username,
                tg_name=message.from_user.first_name,
            )
            await state.finish()

            await message.answer('Account created')
            await message.answer(md.hlink('Get back to web', os.environ["HOST"]))

        except UserAlreadyExist as e:
            await message.answer('User already exists. Try again\nWrite desired username 👇')
    await state.reset_state()
    await Form.username.set()


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
