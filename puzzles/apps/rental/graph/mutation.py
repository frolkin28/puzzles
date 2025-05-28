import strawberry
from django.core.exceptions import PermissionDenied

from puzzles.common.auth import login_required
from puzzles.apps.rental.graph import types as graphql_types
from puzzles.apps.rental.models import Rental, DeliveryType
from puzzles.apps.cart.domain import cart as cart_domain
from puzzles.apps.cart.graph.mapper import graphql_cart_mapper
from puzzles.common.db import AsyncAtomicContextManager
from puzzles.apps.rental.domain import rental as rental_domain
from django.core.exceptions import ValidationError


@strawberry.type(name="Mutation", extend=True)
class RentalMutation:
    @strawberry.mutation
    @login_required
    async def create_rental(
        self,
        delivery_type: graphql_types.GraphQLEnumDeliveryType,
        address: str,
        cart_id: int,
        info: strawberry.Info,
    ) -> graphql_types.Rental | None:
        user = await info.context.request.auser()

        async with AsyncAtomicContextManager():
            stored_cart = await cart_domain.get_cart_by_id(cart_id)
            if not stored_cart or not cart_domain.check_ownership(
                cart=stored_cart,
                user_id=user.id,
                session_id=None,
            ):
                return None

            cart_already_rented = await rental_domain.is_cart_already_rented(
                stored_cart.id
            )
            if cart_already_rented:
                return None

            cart_items = await cart_domain.get_cart_items(stored_cart.id)
            if not cart_items:
                return None

            await cart_domain.persist_items_prices(cart_items)

            rental = Rental(
                cart_id=stored_cart.id,
                user=user,
                rented_due_date=Rental.get_rented_due_date(),
                delivery_type=DeliveryType(delivery_type.value),
                address=address,
            )
            await rental.asave()

        cart = cart_domain.pack_cart(stored_cart.id, cart_items)

        return graphql_types.Rental(
            id=rental.id,
            status=rental.status,
            total_price=cart.total_price,
            total_deposit=cart.total_deposit,
            rented_at=rental.rented_at.isoformat(),
            rented_due_date=rental.rented_due_date.isoformat(),
            returned_at=(
                rental.returned_at.isoformat() if rental.returned_at else None
            ),
            delivery_type=delivery_type,
            address=rental.address,
            cart=graphql_cart_mapper(cart),
        )

    @strawberry.mutation
    @login_required
    async def cancel_rental(
        self,
        rental_id: int,
        info: strawberry.Info,
    ) -> bool:
        user = await info.context.request.auser()
        rental = await Rental.objects.filter(id=rental_id, user=user).afirst()

        if rental:
            await rental.mark_as_cancelled()
            return True
        return False

    @strawberry.mutation
    @login_required
    async def return_rental(
        self,
        rental_id: int,
        verification_photo_urls: list[str],
        info: strawberry.Info,
    ) -> bool:
        user = await info.context.request.auser()
        rental = await Rental.objects.filter(id=rental_id, user=user).afirst()

        if rental:
            await rental.mark_as_returned(verification_photo_urls)
            return True
        else:
            raise PermissionDenied("You do not have permission to return this rental.")
