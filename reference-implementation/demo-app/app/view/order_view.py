"""View: how an order is shown to the customer."""
from app.model.order import Order


def receipt(order: Order) -> str:
    lines = [f"Order for {order.customer}"]
    lines += [f"  {qty} x {name}" for name, qty in order.items.items()]
    lines.append(f"Total: {order.total():.2f}")
    return "\n".join(lines)
