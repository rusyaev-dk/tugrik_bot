from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import choice_horse_callback, place_bid_callback

horse_bid_gamekb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Нобельферто",
                                 callback_data=choice_horse_callback.new(horse_number="0")),
            InlineKeyboardButton(text="Ястреб",
                                 callback_data=choice_horse_callback.new(horse_number="1"))
        ],
        [
            InlineKeyboardButton(text="Ягодка",
                                 callback_data=choice_horse_callback.new(horse_number="2")),
            InlineKeyboardButton(text="Гестер",
                                 callback_data=choice_horse_callback.new(horse_number="3"))
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад",
                                 callback_data=choice_horse_callback.new(horse_number="cancel"))
        ]
    ]
)

place_bidkb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="50",
                                 callback_data=place_bid_callback.new(amount="50")),
            InlineKeyboardButton(text="100",
                                 callback_data=place_bid_callback.new(amount="100"))
        ],
        [
            InlineKeyboardButton(text="250",
                                 callback_data=place_bid_callback.new(amount="250")),
            InlineKeyboardButton(text="500",
                                 callback_data=place_bid_callback.new(amount="500"))
        ],
        [
            InlineKeyboardButton(text="1000",
                                 callback_data=place_bid_callback.new(amount="1000")),
            InlineKeyboardButton(text="2500",
                                 callback_data=place_bid_callback.new(amount="2500"))
        ],
        [
            InlineKeyboardButton(text="5000",
                                 callback_data=place_bid_callback.new(amount="5000"))
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад",
                                 callback_data=place_bid_callback.new(amount="cancel"))
        ]
    ]
)
