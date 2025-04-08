from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import *

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Торговый бот управления",
        reply_markup=main_menu_keyboard()
    )

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 <b>Доступные команды:</b>
/start - Главное меню
/balance - Текущий баланс
/stats - Статистика торговли
"""
    await update.message.reply_text(help_text, parse_mode='HTML')