from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    id: int
    puzzle_id: int
    title: str
    image_url: str | None
    price: str
    deposit: str


@dataclass(frozen=True)
class Cart:
    id: int
    items: tuple[CartItem, ...]
    total_price: str
    total_deposit: str
