import ccxt.pro as ccxt
from typing import Dict, List

class ExchangeClient:
    def __init__(self):
        self.client = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'margin'}
        })

    async def get_market_data(self, symbols: List[str]) -> Dict:
        tasks = [self.client.fetch_ohlcv(s, '1h') for s in symbols]
        return await asyncio.gather(*tasks)
