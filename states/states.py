from aiogram.dispatcher.filters.state import State, StatesGroup

class ChangeTableLink(StatesGroup):
    get_new_link = State()


class TextHandler(StatesGroup):
    get_google_account = State()

