import os
import logging
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from .keyboards import *
from .handlers import *

class TradingBotTelegram:
    def __init__(self, trading_system):
        self.ts = trading_system
        self.app = self.create_app()
        self.register_handlers()

    def create_app(self):
        return ApplicationBuilder() \
            .token(os.getenv("TELEGRAM_TOKEN")) \
            .build()

    def register_handlers(self):
        handlers = [
            CommandHandler('start', handle_start),
            CommandHandler('help', handle_help),
            CommandHandler('balance', handle_balance),
            CallbackQueryHandler(handle_button_click)
        ]
        for handler in handlers:
            self.app.add_handler(handler)

    async def start(self):
        await self.app.run_polling()