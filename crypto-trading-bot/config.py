import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# API Binance
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Настройки бота
SYMBOL = "BTCUSDT"  # Торговая пара
TIMEFRAME = "1h"    # Таймфрейм (1m, 5m, 1h, 4h)
QUANTITY = 0.001    # Сколько BTC покупать

# Telegram уведомления
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
