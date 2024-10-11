from aiogram.fsm.state import StatesGroup, State


class DefaultStates(StatesGroup):
    waiting = State()