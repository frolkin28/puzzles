import strawberry

from puzzles.apps.rental.graph import types as graphql_types
from puzzles.apps.rental.models import Rental
from puzzles.apps.cart.models import CartItem
from puzzles.apps.cart.domain import cart as cart_domain
from puzzles.apps.cart.domain import entity as cart_entity
from puzzles.apps.cart.graph.mapper import graphql_cart_mapper
from puzzles.common.db import iterate_queryset


def make_cart_to_entities_mapping(
    cart_items: list[CartItem],
) -> dict[int, cart_entity.Cart]:
    cart_id_to_cart_items = {}
    for cart_item in cart_items:
        cart_id_to_cart_items.setdefault(cart_item.cart_id, []).append(cart_item)

    return {
        cart_id: cart_domain.pack_cart(cart_id, cart_items)
        for cart_id, cart_items in cart_id_to_cart_items.items()
    }


@strawberry.type(name="Query", extend=True)
class RentalQuery:
    @strawberry.field(description="Get rentals with optional filters")
    async def rentals(
        self,
        info,
        is_for_user: bool = False,
    ) -> list[graphql_types.Rental]:
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
        cart_id_to_cart_entity = make_cart_to_entities_mapping(stored_cart_items)

        return [
            graphql_types.Rental(
                id=rental.id,
                status=rental.status,
                total_price=cart.total_price,
                total_deposit=cart.total_deposit,
                rented_at=rental.rented_at.isoformat(),
                rented_due_date=rental.rented_due_date.isoformat(),
                returned_at=(
                    rental.returned_at.isoformat() if rental.returned_at else None
                ),
                delivery_type=graphql_types.GraphQLEnumDeliveryType(
                    rental.delivery_type
                ),
                address=rental.address,
                cart=graphql_cart_mapper(cart),
            )
            for rental in rentals
            if (cart := cart_id_to_cart_entity.get(rental.cart_id))
        ]
