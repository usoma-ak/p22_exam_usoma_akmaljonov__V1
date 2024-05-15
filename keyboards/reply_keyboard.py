from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard(
        *btns,
        request_contact: int = None,
        request_location: int = None,
        placeholder: int = None,
        sizes: tuple[int] = (2, )
):
    rkb = ReplyKeyboardBuilder()
    for i, text in enumerate(btns):
        if i == request_contact:
            rkb.add(KeyboardButton(text=text, request_contact=True))
        elif i == request_location:
            rkb.add(KeyboardButton(text=text, request_location=True))
        else:
            rkb.add(KeyboardButton(text=text))
    return rkb.adjust(*sizes).as_markup(placeholder=placeholder, resize_keyboard=True)