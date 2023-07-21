import os

from aiogram import Bot, Dispatcher
from aiocryptopay import AioCryptoPay, Networks
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db import Database


ADMIN_ID = 5156872018

bot = Bot("6369843764:AAHaloVXt6JrkdAgNhglbVWN9VP3AMDFMxI")
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()

CRYPTO_API_TOKEN = "109037:AAUf48S2H4nr7dkoR8cluyZzgMH1r9TKddn"
crypto = AioCryptoPay(token=CRYPTO_API_TOKEN, network=Networks.MAIN_NET)

