import logging, asyncio
from config import db, bot, ADMIN_ID


async def check_db():
    while True:
        # logging.warning("function works well")
        users_with_overdue_sub = db.get_users_with_overdue_sub()
        for uid, email, _ in users_with_overdue_sub:
            if not db.is_notified(uid):
                try:
                    await bot.send_message(uid, "Your subscription has been expired. Access to google docs is now forbidden.")
                except:
                    pass
                await bot.send_message(ADMIN_ID, f"! Срок подписки пользователя {uid} c почтой {email} истек.")
                db.set_notified(uid, True)
        await asyncio.sleep(20)
