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
