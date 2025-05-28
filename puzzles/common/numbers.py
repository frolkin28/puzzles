from decimal import Decimal


def stringify_price(price: Decimal) -> str:
    return str(price.quantize(Decimal("0.01")))