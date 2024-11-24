from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 ПОИСК", switch_inline_query_current_chat='')]
        ]
    )

    return kb
