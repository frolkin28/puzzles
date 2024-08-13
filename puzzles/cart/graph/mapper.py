from puzzles.cart.schemas import CartSchema
from puzzles.cart.graph.types import Cart, CartItem


def graphql_cart_mapper(cart: CartSchema) -> Cart:
    return Cart(
        id=cart.id,
        items=[
            CartItem(
                id=item.id,
                puzzleId=item.puzzle_id,
                title=item.title,
                imageUrl=item.image_url,
                price=item.price,
                deposit=item.deposit,
            )
            for item in cart.items
        ],
        totalPrice=cart.total_price,
        totalDeposite=cart.total_deposite,
    )
