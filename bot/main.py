import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from airtable.airtable_manager import create_user, UserAlreadyExist
from config import TOKEN

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)
# fabnum - префикс, action - название аргумента, которым будем передавать значение
# callback_var = CallbackData("proces", "action")
# def get_keyboard_fab():
#     buttons = [
#         types.InlineKeyboardButton(text="-1", callback_data=callback_var.new(action="decr")),
#         types.InlineKeyboardButton(text="+1", callback_data=callback_var.new(action="incr")),
#         types.InlineKeyboardButton(text="Подтвердить", callback_data=callback_var.new(action="finish"))
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard
#
#
# async def regigstration_process(message: types.Message, new_value: int):
#     with suppress(MessageNotModified):
#
#
#         await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard_fab())
# @dp.message_handler(commands="numbers_fab")
# async def cmd_numbers(message: types.Message, user_data=None):
#     user_data[message.from_user.id] = 0
#     await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())
#
# @dp.callback_query_handler(callback_var.filter(action=["incr", "decr"]))
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict, user_data=None):
#     user_value = user_data.get(call.from_user.id, 0)
#     action = callback_data["action"]
#     if action == "incr":
#         user_data[call.from_user.id] = user_value + 1
#         await update_num_text_fab(call.message, user_value + 1)
#     elif action == "decr":
#         user_data[call.from_user.id] = user_value - 1
#         await update_num_text_fab(call.message, user_value - 1)
#     await call.answer()
#
# def text_builder(step_info=None, user_data=None):
#     default_text = 'Your account details:'
#     if user_data is None:
#         default_text = ''
#     build_text = [default_text]
#     new_text = f'\n {step_info}'
#     build_text.append(new_text)
#     return ''.join(build_text)
#
#
# @dp.callback_query_handler(callback_var.filter(action=["reg"]))
# async def registration_start(call: types.CallbackQuery):
#     step_info_txt = 'Input username'
#     await call.message.edit_text(text_builder(step_info=step_info_txt))
#     await call.answer()
#
#
# @dp.message_handler(regexp='^[a-z]+-[0-9]+', content_types=ContentType.TEXT)
# async def get_username(message: types.Message, call: types.CallbackQuery, state: FSMContext):
#     await state.update_data(username=message.text.lower())
#     step_info_txt = 'Input password'
#
#     await call.message.edit_text(text_builder(step_info=step_info_txt))
#     await Registration.username.set()
#
#
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     btn_txt = "Start Registration"
#     buttons = [
#         types.InlineKeyboardButton(text=btn_txt, callback_data=callback_var.new(action="reg")),
#     ]
#     reply_markup = types.InlineKeyboardMarkup()
#     reply_markup.add(*buttons)
#     text = "This bot provides registration for test-task project"
#     await message.answer(text, reply_markup=reply_markup)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    username = State()  # Will be represented in storage as 'Form:name'
    password = State()  # Will be represented in storage as 'Form:age'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.username.set()

    await message.reply("Hi there! input  username?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.username)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['username'] = message.text

    await Form.password.set()
    await message.reply("Input your password")


@dp.message_handler(state=Form.password)
async def process_password(message: types.Message, state: FSMContext):
    # Update state and data
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
            await message.answer(message.link('https://localhost:8000/login'))

        except UserAlreadyExist as e:
            await message.answer('User already exists. Try again')
            await Form.username.set()

    # Configure ReplyKeyboardMarkup

    # await message.reply("Repeat password")


# @dp.message_handler(state='*')
# async def repeat_password(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if message.text == data["password"]:
#             await bot.send_message(
#                 message.chat.id,
#                 md.text(
#                     md.text('Your credentials:'),
#                     md.text('Your login:', md.bold(data['username'])),
#                     md.text('Your password:', md.code(data['password'])),
#                     sep='\n',
#                 ),
#                 parse_mode=ParseMode.MARKDOWN,
#             )
#         else:
#             await process_password(message, state)
#
#     # Finish conversation
#     await state.finish()


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
