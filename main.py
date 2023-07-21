import asyncio

from aiogram import executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from config import bot, dp, db, ADMIN_ID
from markups.markups import (
        main_menu,
        extended_main_menu,
        to_main_menu as tm,
        currencies_menu    
)
from handlers.admin_actions import *
from handlers.process_transaction import *



@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    print("something")
    user_id, msg_text = msg.from_user.id, """Hello, you are using the <b>Affluent Wallets</b> bot. Here you can find the best trading wallets. Use it for <b>copytrading</b> in <b>Maestro</b> or other programs. We select wallets with <b>AI</b> and provide you with the most up-to-date information. For best use we advise you to check the selected wallets in etherscan.io and bscscan.com. You will need a @CryptoBot wallet and a google account to use it"""

    if not db.user_exists(user_id):
        db.add_user(user_id)
    
    kb = main_menu
    if user_id == ADMIN_ID:
        kb = extended_main_menu    
    await bot.send_message(user_id, msg_text, reply_markup=kb, parse_mode="HTML")


@dp.callback_query_handler(lambda x: x.data.startswith("mmenu"))
async def main_menu_handler(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    user_id, has_access = call.from_user.id, db.has_access(call.from_user.id)

    async def process_access_to_table(table_num, tname):
        if has_access:
            with open(f"table{table_num}_link.txt") as f:
                table_link = f.read().rstrip()
            await bot.send_message(user_id, f"Link to table {tname}:\n" + table_link, reply_markup=tm)
        else:
            await bot.send_message(user_id, "You have to pay the access!", reply_markup=tm)

    choice = call.data.split("_")[1]
    match choice:
        case "accesstotable1":
            await process_access_to_table(1, tname="ETH Wallets")
        case "accesstotable2":
            await process_access_to_table(2, tname="BSC Wallets")
        case "makepurchase":
            if has_access:
                await bot.send_message(user_id, "У вас уже есть доступ", reply_markup=tm)
            else:
                await bot.send_message(user_id, "Выберите валюту", reply_markup=currencies_menu)
        case "faq":
            await bot.send_message(user_id, "faq", reply_markup=tm)
        case "changetable":
            await bot.send_message(user_id, "Выберите таблицу, ссылку на которую хотите изменить", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="ETH Wallets", callback_data="changetablelink-1"),
                        InlineKeyboardButton(text="BSC Wallets", callback_data="changetablelink-2")
                    ],
                    [InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")]
                ]
            ))


from functions import check_db

async def on_startup(dp):
    asyncio.create_task(check_db())

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
