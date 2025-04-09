import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

### --- Режим работы (Sandbox или Real) --- ###
TESTNET_MODE = True  # True = тестовая сеть, False = реальная торговля

### --- API Keys --- ###
# Реальные ключи (для основного аккаунта)
REAL_API_KEY = os.getenv("BINANCE_API_KEY")
REAL_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Тестовые ключи (для Sandbox)
TESTNET_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
TESTNET_API_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")

# Автоматический выбор ключей в зависимости от режима
API_KEY = TESTNET_API_KEY if TESTNET_MODE else REAL_API_KEY
API_SECRET = TESTNET_API_SECRET if TESTNET_MODE else REAL_API_SECRET

### --- Настройки бота --- ###
SYMBOL = "BTCUSDT"  # Торговая пара
TIMEFRAME = "1h"    # Таймфрейм (1m, 5m, 1h, 4h)
QUANTITY = 0.001    # Объем для сделки (в BTC)

# Telegram уведомления
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

### --- Binance API URLs (для Sandbox) --- ###
if TESTNET_MODE:
    BINANCE_API_URL = "https://testnet.binance.vision"
else:
    BINANCE_API_URL = "https://api.binance.com"
