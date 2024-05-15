from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_queries import orm_get_user
from filters.chat_types import IsAdmin, ChatTypesFilter

admin_private_router = Router()
admin_private_router.message.filter(ChatTypesFilter(ChatType.PRIVATE), IsAdmin())


class User(StatesGroup):
    user_id = State()
    msg = State()


@admin_private_router.message(or_f(Command(commands='/stat'), F.text.startswith('/stat')))
async def cmd_stat(message: Message, state: FSMContext, session: AsyncSession):
    if len(message.text.split()) == 2 and message.text.split()[1].isalnum():
        try:
            user_info = await orm_get_user(session, int(message.text.split(' ')[-1]))
            if user_info:
                await message.answer(_("User was registered in: {date}").format(date=user_info.created))
            else:
                await message.answer(_("User with this 'id' does not exist."))
        except ValueError:
            await message.answer(_("Enter a proper user id: "))

    else:
        await state.set_state(User.user_id)
        await message.answer(_("Enter a user id: "))


@admin_private_router.message(User.user_id)
async def cmd_stat_userId(message: Message, state: FSMContext, session: AsyncSession):
    try:
        await state.update_data(user_id=message.text)
        data = await state.get_data()
        await state.clear()
        user_info = await orm_get_user(session, int(data['user_id']))
        if user_info:
            await message.answer(_("User was registered in: {date}").format(date=user_info.created))
        else:
            await message.answer(_("User with this 'id' does not exist."))
    except ValueError:
        await message.answer(_("Enter a proper user id: "))


@admin_private_router.message(or_f(Command(commands='/send'), F.text.startswith('/send')))
async def cmd_send(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if len(message.text.split(maxsplit=2)) == 3 and message.text.split()[1].isalnum():
        try:
            user = await orm_get_user(session, int(message.text.split(' ')[1]))
            msg = message.text.split(maxsplit=2)[-1]
            if user:
                await bot.send_message(user.user_id, msg)
            else:
                await message.answer(_("User with this 'id' does not exist."))
        except ValueError:
            await message.answer(_("Enter a proper user id: "))

    else:
        await state.set_state(User.msg)
        await message.answer(_("To send a message to a user enter a user id: "))


@admin_private_router.message(User.user_id)
async def cmd_send_userId(message: Message, state: FSMContext):
    try:
        await state.update_data(user_id=int(message.text))
        await state.set_state(User.msg)
        await message.answer(_("What to send to a user? Enter message: "))
    except ValueError:
        await message.answer(_("Enter a proper user id: "))


@admin_private_router.message(User.msg)
async def cmd_send_msg(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(msg=message.text)
    data = await state.get_data()
    await bot.send_message(data['user_id'], data['msg'])
    await state.clear()
    await message.answer(_("Message has been sent"))
