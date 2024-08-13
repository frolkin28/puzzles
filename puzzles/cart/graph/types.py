import strawberry


@strawberry.type
class CartItem:
    id: int
    puzzleId: int
    title: str
    imageUrl: str | None
    price: str
    deposit: str


@strawberry.type
class Cart:
    id: int
    items: list[CartItem]
    totalPrice: str
    totalDeposite: str
