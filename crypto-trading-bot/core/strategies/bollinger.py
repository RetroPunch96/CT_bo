import pandas as pd
from typing import Optional
from ..common import TradeSignal

class BollingerBandsStrategy:
    def __init__(self):
        self.period = 20
        self.std_dev = 2

    async def analyze(self, ohlcv: pd.DataFrame) -> Optional[TradeSignal]:
        df = ohlcv.copy()
        df['ma'] = df['close'].rolling(self.period).mean()
        df['std'] = df['close'].rolling(self.period).std()
        df['upper'] = df['ma'] + (df['std'] * self.std_dev)
        df['lower'] = df['ma'] - (df['std'] * self.std_dev)
        
        last = df.iloc[-1]
        if last['close'] <= last['lower']:
            return TradeSignal(
                symbol=ohlcv.symbol,
                side='buy',
                confidence=0.65
            )
        return None
