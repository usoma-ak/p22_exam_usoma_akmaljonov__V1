from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2, )
):
    ikb = InlineKeyboardBuilder()
    for text, value in btns.items():
        if '://' in value:
            ikb.add(InlineKeyboardButton(text=text, url=value))
        else:
            ikb.add(InlineKeyboardButton(text=text, callback_data=value))
    return ikb.adjust(*sizes).as_markup()
