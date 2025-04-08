import asyncio
from core.trading_system import TradingSystem
from telegram.bot import TradingBotTelegram

class CryptoTradingBot:
    def __init__(self):
        self.ts = TradingSystem()
        self.telegram_bot = TradingBotTelegram(self.ts)

    async def run(self):
        await self.telegram_bot.start()
        await self.ts.run()

if __name__ == "__main__":
    bot = CryptoTradingBot()
    asyncio.run(bot.run())

from core.trading_system import TradingSystem
from telegram.bot import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()

class CryptoBot:
    def __init__(self):
        self.trading_system = TradingSystem()
        self.telegram_bot = TelegramBot(
            token=os.getenv("TELEGRAM_TOKEN"),
            trading_bot=self
        )
    
    def start(self):
        self.trading_system.start()
        self.telegram_bot.start()
    
    def stop(self):
        self.trading_system.stop()
        self.telegram_bot.stop()

if __name__ == "__main__":
    bot = CryptoBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.stop()
