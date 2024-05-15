from aiogram import Router, F
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_queries import orm_add_user
from filters.chat_types import ChatTypesFilter
from keyboards.inline_keyboard import get_inline_keyboard
from keyboards.reply_keyboard import get_reply_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter([ChatType.PRIVATE]))


@user_private_router.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    await message.answer(_("Hello {name}, welcome to my bot 😇").format(
        name=message.from_user.mention_markdown(message.from_user.first_name)),
        reply_markup=(get_reply_keyboard(_('🌐 Choose a language'))), parse_mode=ParseMode.MARKDOWN_V2)
    await orm_add_user(session, message.from_user.id)


@user_private_router.message(F.text == __("🌐 Choose a language"))
async def choose_language(message: Message):
    await message.answer(_("Choose: "), reply_markup=get_inline_keyboard(btns={
        "En 🇬🇧": "lang_en",
        "Uz 🇺🇿": "lang_uz"
    }))


@user_private_router.callback_query(F.data.startswith("lang"))
async def language(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[-1]
    await state.update_data(locale=lang_code)
    language = (_("Uzbek", locale='uz'), _("English", locale='en'))[lang_code == 'en']
    await callback.answer(_('{language} is selected', locale=lang_code).format(language=language))
    await callback.message.answer(_("Choose:"), reply_markup=get_reply_keyboard(
        _("🌐 Choose a language", locale=lang_code)
    ))
