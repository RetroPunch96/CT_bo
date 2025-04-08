import pandas as pd
from typing import Optional
from ..common import TradeSignal

class RSIStrategy:
    def __init__(self):
        self.period = 14
        self.oversold = 30
        self.overbought = 70

    async def analyze(self, ohlcv: pd.DataFrame) -> Optional[TradeSignal]:
        delta = ohlcv['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        if rsi.iloc[-1] < self.oversold:
            return TradeSignal(symbol=ohlcv.symbol, side='buy', confidence=0.6)
        elif rsi.iloc[-1] > self.overbought:
            return TradeSignal(symbol=ohlcv.symbol, side='sell', confidence=0.6)
        return None
