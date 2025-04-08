from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("💰 Баланс", callback_data='balance')],
        [InlineKeyboardButton("📊 Статистика", callback_data='stats')]
    ]
    return InlineKeyboardMarkup(buttons)