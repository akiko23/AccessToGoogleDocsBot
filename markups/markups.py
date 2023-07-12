from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Таблица 1", callback_data="mmenu_accesstotable1"),
            InlineKeyboardButton(text="Таблица 2", callback_data="mmenu_accesstotable2")
        ],
        [
            InlineKeyboardButton(text="Оплата", callback_data="mmenu_makepurchase"),
            InlineKeyboardButton(text="FAQ", callback_data="mmenu_faq")
        ],
    ]
)

to_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")],
        ]
)

currencies_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Usdt", callback_data="currency_usdt_trc"),
        ],
        [
            InlineKeyboardButton(text="Eth", callback_data="currency_eth_eth"),
        ],
        [
            InlineKeyboardButton(text="Busd", callback_data="currency_busd_bsc"),
            InlineKeyboardButton(text="Bnb", callback_data="currency_bnb_bsc"),
        ],
        [InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")]
    ]
)

cancel_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel_changing"),
        ]
    ]
)

