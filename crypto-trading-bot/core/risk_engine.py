from typing import Dict
from .common import TradeSignal

class RiskEngine:
    def __init__(self):
        self.max_drawdown = 0.15  # 15%
        self.max_risk_per_trade = 0.02  # 2%

    def validate_trade(self, signal: TradeSignal, portfolio: Dict) -> bool:
        if signal.confidence < 0.5:
            return False
            
        risk_amount = portfolio['balance'] * self.max_risk_per_trade
        if signal.estimated_loss > risk_amount:
            return False
            
        return True
