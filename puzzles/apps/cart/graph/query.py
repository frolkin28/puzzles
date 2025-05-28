from puzzles.apps.cart.graph.mapper import graphql_cart_mapper
import strawberry

from puzzles.apps.cart.graph.types import Cart
from puzzles.apps.cart.domain import cart as cart_domain
from puzzles.common.auth import extract_user_identifier


@strawberry.type(name="Query", extend=True)
class CartQuery:
    @strawberry.field
    async def shopping_cart(
        self,
        info: strawberry.Info,
    ) -> Cart | None:
        user_id, session_id = await extract_user_identifier(info.context.request)
        cart = await cart_domain.get_shopping_cart(
            user_id=user_id,
            session_id=session_id,
        )
        return graphql_cart_mapper(cart) if cart else None
