import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, BotCommandScopeType
from aiogram.types import BotCommandScopeAllChatAdministrators, BotCommandScopeAllPrivateChats
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

from common.cmd_list import user_commands, admin_commands
from common.routers import start_router
from config import TOKEN, ADMINS
from database.engine import session_maker, create_db, drop_db
from middlewares.db import DataBaseSession

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_routers(start_router)


async def on_startup():
    # await drop_db()
    await create_db()
    await bot.set_my_commands(user_commands)
    for i in ADMINS:
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeAllPrivateChats())


async def on_shutdown():
    await bot.delete_my_commands()


async def main():
    dp.startup.register(on_startup)
    dp.startup.register(on_shutdown)
    dp.update.outer_middleware(FSMI18nMiddleware(I18n(path='locales')))
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
