from typing import Annotated

from puzzles.cart.graph.mapper import graphql_cart_mapper
import strawberry

from puzzles.cart.graph.types import Cart
from puzzles.cart.lib import (
    add_item_to_cart,
    remove_item_from_cart,
    extract_user_identifier,
)


@strawberry.type(name="Mutation", extend=True)
class CartMutation:
    @strawberry.mutation
    async def add_cart_item(
        self,
        info: strawberry.Info,
        puzzle_id: Annotated[
            int,
            strawberry.argument(name="id"),
        ],
    ) -> Cart | None:
        user_id, session_id = await extract_user_identifier(info.context.request)
        cart = await add_item_to_cart(
            user_id=user_id,
            session_id=session_id,
            puzzle_id=puzzle_id,
        )
        return graphql_cart_mapper(cart) if cart else None

    @strawberry.mutation
    async def remove_cart_item(
        self,
        info: strawberry.Info,
        item_id: Annotated[
            int,
            strawberry.argument(name="itemId"),
        ],
    ) -> Cart | None:
        user_id, session_id = await extract_user_identifier(info.context.request)
        cart = await remove_item_from_cart(
            user_id=user_id,
            session_id=session_id,
            item_id=item_id,
        )
        return graphql_cart_mapper(cart) if cart else None
