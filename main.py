import json

from aiogram import executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from config import bot, dp, db, crypto, ADMIN_ID
from markups.markups import (
        main_menu, 
        to_main_menu as tm,
        currencies_menu,
        cancel_keyb
)
from functions import get_onetime_link
from states.states import ChangeTableLink


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user_id = msg.from_user.id
    if not db.user_exists(user_id):
        db.add_user(user_id)
    if user_id == ADMIN_ID:
        extended_main_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Таблица 1", callback_data="mmenu_accesstotable1"),
                    InlineKeyboardButton(text="Таблица 2", callback_data="mmenu_accesstotable2")
                ],
                [
                    InlineKeyboardButton(text="Оплата", callback_data="mmenu_makepurchase"),
                    InlineKeyboardButton(text="FAQ", callback_data="mmenu_faq")
                ],
                [InlineKeyboardButton(text="Изменить таблицу", callback_data="mmenu_changetable")]
            ]
        )
        await bot.send_message(user_id, "Test", reply_markup=extended_main_menu)
    else:
        await bot.send_message(user_id, "Test", reply_markup=main_menu)


@dp.callback_query_handler(lambda x: x.data.startswith("mmenu"))
async def main_menu_handler(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    user_id, has_access = call.from_user.id, db.has_access(call.from_user.id)
    
    with open("table1_link.txt") as f1, open("table2_link.txt") as f2:
        table1_link, table2_link = f1.read().rstrip(), f2.read().rstrip()

    async def process_access_to_table(table_link):
        if has_access:
            link = await get_onetime_link(table_link)
            await bot.send_message(user_id, "One time link to table:\n" + link, reply_markup=tm)
        else:
            await bot.send_message(user_id, "Для начала оплатите доступ", reply_markup=tm)

    choice = call.data.split("_")[1]
    match choice:
        case "accesstotable1":
            await process_access_to_table(table1_link)
        case "accesstotable2":
            await process_access_to_table(table2_link)
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
                        InlineKeyboardButton(text="Таблица 1", callback_data="changetablelink-1"),
                        InlineKeyboardButton(text="Таблица 2", callback_data="changetablelink-2")
                    ],
                    [InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")]
                ]
            ))


@dp.callback_query_handler(lambda call: call.data.startswith("currency"))
async def process_payment(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.delete_message(user_id, call.message.message_id) 
    
    with open("current_transactions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if data.get(str(user_id)):
        if db.has_access(user_id):
            await bot.send_message(user_id, "У вас уже есть доступ", reply_markup=tm)
        else:
            await bot.send_message(user_id, "Вы не можете создавать сделку, пока не закрыли предыдущую")
        return
    
    coin = call.data.split("_")[1]
    invoice = await crypto.create_invoice(asset=coin, amount=0.4, payload=f"{user_id}")

    data[user_id] = invoice.invoice_id    
    with open("current_transactions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    await bot.send_message(user_id, "Оплатите", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Оплатить", url=invoice.pay_url)]
            ]
        ))
    await bot.send_message(user_id, "Выберите действие", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Подтвердить оплату", callback_data="transaction_submit"),
                InlineKeyboardButton("Отмена", callback_data="transaction_cancel")
            ]
        ]
    ))

@dp.callback_query_handler(lambda call: call.data.startswith("transaction"))
async def process_action_with_transaction(call: types.CallbackQuery):
    user_id, action = call.from_user.id, call.data.split("_")[1]
    with open("current_transactions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if action == "submit":
        user_last_invoice = await crypto.get_invoices(invoice_ids=data[str(user_id)])

        if user_last_invoice.status == "paid":
            db.set_access(user_id)
            await bot.send_message(user_id, "Вы успешно приобрели доступ на одну неделю", reply_markup=tm)
        else:
            await bot.send_message(user_id, "Вы не совершили оплату")
    else:
        with open("current_transactions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                del data[str(user_id)]
        json.dump(data, open("current_transactions.json", "w", encoding="utf-8"))
        await bot.send_message(user_id, "Процесс покупки отменен", reply_markup=tm)


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

    if call.from_user.id == ADMIN_ID:
        extended_main_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Таблица 1", callback_data="mmenu_accesstotable1"),
                    InlineKeyboardButton(text="Таблица 2", callback_data="mmenu_accesstotable2")
                ],
                [
                    InlineKeyboardButton(text="Оплата", callback_data="mmenu_makepurchase"),
                    InlineKeyboardButton(text="FAQ", callback_data="mmenu_faq")
                ],
                [InlineKeyboardButton(text="Изменить таблицу", callback_data="mmenu_changetable")]
            ]
        )
        await bot.send_message(call.from_user.id, "Вы вернулись в главное меню", reply_markup=extended_main_menu)
    else:
        await bot.send_message(call.from_user.id, "Вы вернулись в главное меню", reply_markup=main_menu)


# def worker():
#     try:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         loop.run_until_complete()
#     finally:
#         loop.close()

def main():
    executor.start_polling(dp, skip_updates=True)     

if __name__ == "__main__":
    main()
