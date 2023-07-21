from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from config import bot, dp, db, ADMIN_ID
from markups.markups import (
        main_menu,
        extended_main_menu,
        to_main_menu as tm,
        cancel_keyb
)
from states.states import ChangeTableLink


__all__ = ["get_new_link", "change_table_link", "cancel_changing", "back_to_main_menu"]

@dp.callback_query_handler(lambda call: call.data.startswith("changetablelink"))
async def get_new_link(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    table_num = call.data[-1]
    ChangeTableLink.get_new_link.__dict__["table_num"] = table_num

    await bot.send_message(call.from_user.id, "Ввведите новую ссылку", reply_markup=cancel_keyb)
    await ChangeTableLink.get_new_link.set()
    

@dp.message_handler(content_types=["text"], state=ChangeTableLink.get_new_link)
async def change_table_link(msg: types.Message, state):
    new_link = msg.text
    table_num = ChangeTableLink.get_new_link.__dict__["table_num"]
    with open("table" + table_num + "_link.txt", "w") as f:
        f.write(new_link)
    
    db.reset_access()
    await bot.send_message(msg.from_user.id, "Ссылка успешно изменена!", reply_markup=tm)
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == "cancel_changing", state=ChangeTableLink.get_new_link)
async def cancel_changing(call, state):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    await state.finish()
    await bot.send_message(call.from_user.id, "Вы отменили процесс изменения", reply_markup=tm)

@dp.callback_query_handler(lambda call: call.data == "to_main_menu")
async def back_to_main_menu(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    kb = main_menu
    if call.from_user.id == ADMIN_ID:
        kb = extended_main_menu
    await bot.send_message(call.from_user.id, "You returned to main menu", reply_markup=kb)
