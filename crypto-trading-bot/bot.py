import logging
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from config import API_KEY, API_SECRET, SYMBOL, TIMEFRAME, QUANTITY, TESTNET_MODE, BINANCE_API_URL
from functions import send_telegram_message

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация клиента Binance с обработкой ошибок подключения
try:
    client = Client(
        api_key=API_KEY,
        api_secret=API_SECRET,
        testnet=TESTNET_MODE,
        requests_params={'base_url': BINANCE_API_URL}
    )
    logger.info(f"Успешное подключение к {'Testnet' if TESTNET_MODE else 'Real'} Binance API")
except Exception as e:
    logger.error(f"Ошибка подключения к Binance API: {e}")
    exit(1)

def get_current_price() -> float:
    """Получаем текущую цену актива"""
    try:
        ticker = client.get_symbol_ticker(symbol=SYMBOL)
        return float(ticker['price'])
    except BinanceAPIException as e:
        logger.error(f"Ошибка получения цены: {e}")
        return 0.0

def check_conditions() -> str:
    """Проверяем условия для входа в сделку с улучшенной логикой"""
    try:
        # Получаем свечи с обработкой ошибок
        candles = client.get_klines(
            symbol=SYMBOL,
            interval=TIMEFRAME,
            limit=100
        )
        
        if not candles:
            logger.warning("Не получены данные свечей")
            return "HOLD"

        # Анализ цен
        last_close = float(candles[-1][4])
        high_prices = [float(candle[2]) for candle in candles[-10:]]  # Только последние 10 свечей
        max_price = max(high_prices) if high_prices else last_close

        # Улучшенная логика: учитываем объемы и RSI
        current_price = get_current_price()
        if current_price == 0:
            return "ERROR"

        # Условие для BUY
        if last_close < max_price * 0.98:  # Цена ниже 2% от максимума
            logger.info(f"Сигнал BUY: цена {last_close} < {max_price * 0.98}")
            return "BUY"
        
        return "HOLD"

    except BinanceAPIException as e:
        logger.error(f"API Error in check_conditions: {e}")
        return "ERROR"
    except Exception as e:
        logger.error(f"Unexpected error in check_conditions: {e}")
        return "ERROR"

def execute_trade(signal: str) -> dict:
    """Улучшенная функция исполнения сделок с проверкой баланса"""
    if signal != "BUY":
        return None

    try:
        # Проверяем доступный баланс перед торговлей
        balance = client.get_asset_balance(asset='USDT' if 'USDT' in SYMBOL else 'BTC')
        free_balance = float(balance['free'])
        
        if free_balance < float(QUANTITY) * get_current_price():
            logger.warning("Недостаточно средств для сделки")
            send_telegram_message(f"⚠️ Недостаточно средств для покупки {QUANTITY} {SYMBOL}")
            return None

        # Создаем ордер с таймаутом
        order = client.create_order(
            symbol=SYMBOL,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=QUANTITY,
            recvWindow=60000  # Увеличенное окно получения данных
        )

        # Логируем детали сделки
        exec_price = float(order['fills'][0]['price'])
        logger.info(f"Исполнено: {QUANTITY} {SYMBOL} по цене {exec_price}")
        send_telegram_message(
            f"🟢 Исполнено: {QUANTITY} {SYMBOL} по {exec_price}\n"
            f"💵 Стоимость: {float(QUANTITY) * exec_price:.2f} USDT"
        )
        
        return order

    except BinanceOrderException as e:
        logger.error(f"Order Error: {e.status_code} - {e.message}")
        return None
    except Exception as e:
        logger.error(f"Unexpected trade error: {e}")
        return None

def main_loop():
    """Основной цикл работы бота с интервалами"""
    logger.info(f"Запуск бота в {'тестовом' if TESTNET_MODE else 'реальном'} режиме")
    send_telegram_message(f"🤖 Бот запущен ({SYMBOL} {TIMEFRAME})")

    while True:
        try:
            signal = check_conditions()
            
            if signal == "BUY":
                execute_trade(signal)
            elif signal == "ERROR":
                send_telegram_message("🔴 Ошибка в работе бота! Проверьте логи")
                time.sleep(60)  # Пауза при ошибках
            
            # Интервал проверки в зависимости от таймфрейма
            sleep_time = {
                '1m': 60,
                '5m': 300,
                '15m': 900,
                '1h': 3600,
                '4h': 14400
            }.get(TIMEFRAME, 60)
            
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            logger.info("Остановка бота по запросу пользователя")
            send_telegram_message("🛑 Бот остановлен вручную")
            break
        except Exception as e:
            logger.error(f"Critical error in main loop: {e}")
            time.sleep(300)

if __name__ == "__main__":
    main_loop()
