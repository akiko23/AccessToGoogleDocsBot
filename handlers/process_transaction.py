import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from config import bot, dp, db, crypto, ADMIN_ID
from markups.markups import (
        to_main_menu as tm,
        cancel_keyb
)
from states.states import TextHandler


__all__ = ["process_payment", "process_action_with_transaction", "process_google_account", "process_access"]

@dp.callback_query_handler(lambda call: call.data.startswith("currency"))
async def process_payment(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.delete_message(user_id, call.message.message_id) 
    
    with open("current_transactions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if data.get(str(user_id)):
        if db.has_access(user_id):
            await bot.send_message(user_id, "You already have the access", reply_markup=tm)
        else:
            await bot.send_message(user_id, "You can not create a new transaction until you complete another one")
        return
    
    coin = call.data.split("_")[1]
    invoice = await crypto.create_invoice(asset=coin, amount=0.4, payload=f"{user_id}")

    data[user_id] = invoice.invoice_id    
    with open("current_transactions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    await bot.send_message(user_id, "You need to follow the link below and pay via @CryptoBot", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Pay", url=invoice.pay_url)]
            ]
        ))
    await bot.send_message(user_id, "Choose the action", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Submit", callback_data="transaction_submit"),
                InlineKeyboardButton("Cancel", callback_data="transaction_cancel")
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
            await bot.send_message(user_id, "You'll need to provide a google account. Enter the email", reply_markup=cancel_keyb)
            await TextHandler.get_google_account.set()
        else:
            await bot.send_message(user_id, "You didn't pay for access")
    else:
        await bot.delete_message(user_id, call.message.message_id)
        with open("current_transactions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                del data[str(user_id)]
        json.dump(data, open("current_transactions.json", "w", encoding="utf-8"))
        await bot.send_message(user_id, "You canceled the payment process", reply_markup=tm)

@dp.message_handler(content_types=["text"], state=TextHandler.get_google_account)
async def process_google_account(msg: types.Message, state):
    await bot.send_message(ADMIN_ID, f"Гугл аккаунт юзера @{msg.from_user.username} с id {msg.from_user.id}: {msg.text}", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Подтвердить", callback_data=f"access-allow-{msg.from_user.id}-{msg.text}"),
                InlineKeyboardButton("Отклонить", callback_data=f"access-refuse-{msg.from_user.id}-{msg.text}"),
            ]
        ]
    ))
    await bot.send_message(msg.from_user.id, "Your email was forward to admin. Now, wait for the response :)")
    await state.finish()

@dp.callback_query_handler(lambda call: call.data.startswith("access"))
async def process_access(call: types.CallbackQuery):
    _, action, user_id, email = call.data.split("-")
    if action == "allow":
        db.set_access(user_id, email)

        await bot.send_message(ADMIN_ID, f"Доступ юзеру {user_id} открыт")
        await bot.send_message(user_id, "Finally, you get an access to both tables for a one week", reply_markup=tm)
    else:
        await bot.send_message(user_id, "Admin denied your request")
