from puzzles.account.lib import login_required
import strawberry

from asgiref.sync import sync_to_async
from puzzles.rental.graph.types import (
    RentalType,
    GraphQLEnumDeliveryType,
)
from puzzles.rental.models import Rental
from puzzles.cart.models import Cart
from puzzles.cart.lib import pack_cart
from puzzles.cart.graph.mapper import graphql_cart_mapper


@strawberry.type
class RentalQuery:
    @strawberry.field(description="Get rentals with optional filters")
    @login_required
    async def rentals(
        self,
        info,
        is_for_user: bool = False,
    ) -> list[RentalType]:
        user = await info.context.request.auser()

        if is_for_user:
            if not user.is_authenticated:
                raise Exception("User not authenticated")
            rentals = await sync_to_async(Rental.objects.filter(user=user).all)()
        else:
            rentals = await sync_to_async(Rental.objects.all)()

        carts_query = await sync_to_async(
            Cart.objects.prefetch_related("cart_items", "cart_items__item").filter(
                id__in=[rental.cart_id for rental in rentals]
            )
        )()
        carts_map = {cart.id: cart for cart in carts_query}

        def get_graphql_cart(cart_id: int):
            if cart := carts_map.get(cart_id):
                return graphql_cart_mapper(pack_cart(cart))
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
