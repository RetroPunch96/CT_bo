from dataclasses import dataclass
from typing import Optional

@dataclass
class TradeSignal:
    symbol: str
    side: str  # 'buy' or 'sell'
    amount: Optional[float] = None
    confidence: float = 1.0
    timestamp: Optional[int] = None
