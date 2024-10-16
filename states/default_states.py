from aiogram.fsm.state import StatesGroup, State


class DefaultStates(StatesGroup):
    waiting_photo = State()
    waiting_delete = State()
    waiting_admin = State()
    waiting_user = State()
