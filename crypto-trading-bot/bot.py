
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET, SYMBOL, TIMEFRAME, QUANTITY
from functions import send_telegram_message

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Инициализация клиента Binance
client = Client(API_KEY, API_SECRET)

def check_conditions():
    """Проверяем условия для входа в сделку"""
    try:
        # Получаем свечи
        candles = client.get_klines(symbol=SYMBOL, interval=TIMEFRAME, limit=100)
        last_close = float(candles[-1][4])  # Цена закрытия последней свечи

        # Простая стратегия: покупаем, если цена упала на 2% от максимума
        high_prices = [float(candle[2]) for candle in candles]
        max_price = max(high_prices[-10:])  # Максимум за последние 10 свечей
        if last_close < max_price * 0.98:  # Если цена ниже на 2%
            return "BUY"
        else:
            return "HOLD"

    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e}")
        return "ERROR"

def execute_trade(signal):
    """Отправляем ордер на Binance"""
    try:
        if signal == "BUY":
            order = client.create_order(
                symbol=SYMBOL,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=QUANTITY
            )
            logger.info(f"Куплено {QUANTITY} {SYMBOL}")
            send_telegram_message(f"🟢 Куплено {QUANTITY} {SYMBOL} по цене {order['fills'][0]['price']}")
            return order
    except Exception as e:
        logger.error(f"Trade Error: {e}")
        return None

if __name__ == "__main__":
    logger.info("Бот запущен")
    signal = check_conditions()
    if signal == "BUY":
        execute_trade(signal)
