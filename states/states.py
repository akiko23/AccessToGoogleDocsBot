from aiogram.dispatcher.filters.state import State, StatesGroup

class ChangeTableLink(StatesGroup):
    get_new_link = State()

