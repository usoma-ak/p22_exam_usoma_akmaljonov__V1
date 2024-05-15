from aiogram.filters import Filter
from aiogram.types import Message

from config import ADMINS


class ChatTypesFilter(Filter):
    def __init__(self, chat_types) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS
