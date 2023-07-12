import os

from aiogram import Bot, Dispatcher
from aiocryptopay import AioCryptoPay, Networks
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from db import Database


bot = Bot(os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()

CRYPTO_API_TOKEN = os.environ.get("CRYPTO_BOT_TOKEN")
crypto = AioCryptoPay(token=CRYPTO_API_TOKEN, network=Networks.MAIN_NET)

