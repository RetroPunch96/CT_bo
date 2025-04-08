import pandas as pd
from typing import Optional
from ..common import TradeSignal

class EMAMACDStrategy:
    def __init__(self):
        self.ema_fast = 12
        self.ema_slow = 26
        self.signal_period = 9

    async def analyze(self, ohlcv: pd.DataFrame) -> Optional[TradeSignal]:
        df = ohlcv.copy()
        df['ema_fast'] = df['close'].ewm(span=self.ema_fast).mean()
        df['ema_slow'] = df['close'].ewm(span=self.ema_slow).mean()
        macd = df['ema_fast'] - df['ema_slow']
        signal = macd.ewm(span=self.signal_period).mean()
        
        last = df.iloc[-1]
        if macd.iloc[-1] > signal.iloc[-1] and last['ema_fast'] > last['ema_slow']:
            return TradeSignal(
                symbol=ohlcv.symbol,
                side='buy',
                confidence=0.7
            )
        return None
