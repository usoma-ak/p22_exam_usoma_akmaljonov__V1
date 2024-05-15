from aiogram.types import BotCommand

user_commands = [
    BotCommand(command='start', description='🚀 Starts the bot'),
    BotCommand(command='help', description='⚙ Do you need a help?')
]


admin_commands = [
    BotCommand(command='/stat', description='📆 Show register statistics'),
    BotCommand(command='/send', description='📨 Send a message to user')
]