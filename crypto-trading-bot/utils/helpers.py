from typing import Union

def calculate_pnl(entry: float, exit: float, amount: float) -> float:
    return (exit - entry) * amount

def format_price(price: Union[float, str], precision: int = 8) -> str:
    return f"{float(price):.{precision}f}"
