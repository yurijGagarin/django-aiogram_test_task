from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    username = State()
    password = State()
    username_id = State()
