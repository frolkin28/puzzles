from puzzles.cart.graph.mapper import graphql_cart_mapper
import strawberry

from puzzles.cart.graph.types import Cart
from puzzles.cart.lib import extract_user_identifier, get_shopping_cart


@strawberry.type(name="Query", extend=True)
class CartQuery:
    @strawberry.field
    async def shopping_cart(
        self,
        info: strawberry.Info,
    ) -> Cart | None:
        user_id, session_id = await extract_user_identifier(info.context.request)
        cart = await get_shopping_cart(
            user_id=user_id,
            session_id=session_id,
        )
        return graphql_cart_mapper(cart) if cart else None
