from puzzles.apps.cart.domain import entity
from puzzles.apps.cart.graph import types


def graphql_cart_mapper(cart: entity.Cart) -> types.Cart:
    return types.Cart(
        id=cart.id,
        items=[
            types.CartItem(
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
        totalDeposit=cart.total_deposit,
    )
