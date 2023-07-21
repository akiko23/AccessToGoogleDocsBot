from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ETH Wallets", callback_data="mmenu_accesstotable1"),
            InlineKeyboardButton(text="BSC Wallets", callback_data="mmenu_accesstotable2")
        ],
        [
            InlineKeyboardButton(text="Payment", callback_data="mmenu_makepurchase"),
            InlineKeyboardButton(text="FAQ", callback_data="mmenu_faq")
        ],
    ]
)

extended_main_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="ETH Wallets", callback_data="mmenu_accesstotable1"),
                    InlineKeyboardButton(text="BSC Wallets", callback_data="mmenu_accesstotable2")
                ],
                [
                    InlineKeyboardButton(text="Payment", callback_data="mmenu_makepurchase"),
                    InlineKeyboardButton(text="FAQ", callback_data="mmenu_faq")
                ],
                [InlineKeyboardButton(text="Изменить таблицу", callback_data="mmenu_changetable")]
            ]
        )

to_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="To main menu", callback_data="to_main_menu")],
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
        [InlineKeyboardButton(text="To main menu", callback_data="to_main_menu")]
    ]
)

cancel_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cancel", callback_data="cancel_changing"),
        ]
    ]
)

