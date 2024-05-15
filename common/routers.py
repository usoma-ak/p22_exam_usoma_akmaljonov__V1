from aiogram import Router

from handlers.admin_private import admin_private_router
from handlers.user_private import user_private_router

start_router = Router()

start_router.include_routers(
    user_private_router,
    admin_private_router,
)
