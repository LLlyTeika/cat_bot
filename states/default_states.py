from aiogram.fsm.state import StatesGroup, State


class DefaultStates(StatesGroup):
    waiting_photo = State()
    waiting_admin = State()