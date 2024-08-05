from pydantic import BaseModel


class CartItemSchema(BaseModel):
    id: int
    puzzle_id: int
    title: str
    image_url: str | None
    price: str
    deposit: str


class CartSchema(BaseModel):
    id: int
    items: tuple[CartItemSchema]
    total_price: str
    total_deposite: str
