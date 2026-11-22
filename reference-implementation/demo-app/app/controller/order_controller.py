"""Controller: turns a request into an order."""
from app.model.order import PRICES, Order


def place_order(customer: str, items: dict) -> Order:
    unknown = [name for name in items if name not in PRICES]
    if unknown:
        raise ValueError(f"unknown product(s): {', '.join(unknown)}")
    return Order(customer=customer, items=dict(items))
