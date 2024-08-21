import strawberry

from puzzles.rental.graph.types import (
    RentalType,
    GraphQLEnumDeliveryType,
)
from puzzles.rental.models import Rental
from puzzles.cart.models import Cart, CartItem
from puzzles.cart.lib import pack_cart
from puzzles.cart.graph.mapper import graphql_cart_mapper
from puzzles.utils.db import iterate_queryset


def make_cart_items_map(cart_items: list[CartItem]) -> dict[int, list[CartItem]]:
    items_mapping = {}
    for cart_item in cart_items:
        items_mapping.setdefault(cart_item.cart_id, []).append(cart_item)

    return items_mapping


@strawberry.type
class RentalQuery:
    @strawberry.field(description="Get rentals with optional filters")
    async def rentals(
        self,
        info,
        is_for_user: bool = False,
    ) -> list[RentalType]:
        user = await info.context.request.auser()

        if is_for_user:
            if not user.is_authenticated:
                raise Exception("User not authenticated")
            rentals = await iterate_queryset(Rental.objects.filter(user=user))
        else:
            rentals = await iterate_queryset(Rental.objects.all())

        cart_ids = [rental.cart_id for rental in rentals]

        stored_cart_items = await iterate_queryset(
            CartItem.objects.filter(cart_id__in=cart_ids).select_related("item")
        )
        cart_items_map = make_cart_items_map(stored_cart_items)

        def get_graphql_cart(cart_id: int):
            if cart_items := cart_items_map.get(cart_id):
                return graphql_cart_mapper(pack_cart(cart_id, cart_items))
            return None

        return [
            RentalType(
                id=rental.id,
                status=rental.status,
                total_price=rental.total_price,
                total_deposit=rental.total_deposit,
                rented_at=rental.rented_at.isoformat(),
                rented_due_date=rental.rented_due_date.isoformat(),
                returned_at=(
                    rental.returned_at.isoformat() if rental.returned_at else None
                ),
                delivery_type=GraphQLEnumDeliveryType(rental.delivery_type),
                address=rental.address,
                cart=get_graphql_cart(rental.cart_id),
            )
            for rental in rentals
        ]
