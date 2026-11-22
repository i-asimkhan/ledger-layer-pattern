"""Model: a fictional bakery order."""
from dataclasses import dataclass, field

PRICES = {"sourdough": 6.50, "croissant": 3.25, "baguette": 4.00}


@dataclass
class Order:
    customer: str
    items: dict = field(default_factory=dict)  # product -> quantity

    def total(self) -> float:
        return round(sum(PRICES[name] * qty for name, qty in self.items.items()), 2)
