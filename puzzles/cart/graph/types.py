import strawberry


@strawberry.type
class CartItem:
    id: int
    puzzleId: int
    title: str
    imageUrl: str | None
    price: str
    deposit: str
    verificationPhoto: str | None = None


@strawberry.type
class Cart:
    id: int
    items: list[CartItem]
    totalPrice: str
    totalDeposite: str
