import strawberry
from datetime import datetime, timedelta

from django.core.exceptions import PermissionDenied
from django.db import transaction

from puzzles.account.lib import login_required
from puzzles.rental.graph.types import RentalType, GraphQLEnumDeliveryType
from puzzles.rental.models.rental import Rental, DeliveryType
from puzzles.cart.lib import (
    get_cart_by_id,
    check_ownership,
    get_cart_items,
    persist_items_prices,
    pack_cart,
)
from puzzles.cart.graph.mapper import graphql_cart_mapper


@strawberry.type
class RentalMutation:
    @strawberry.mutation
    @login_required
    async def create_rental(
        self,
        delivery_type: GraphQLEnumDeliveryType,
        address: str,
        cart_id: int,
        info: strawberry.Info,
    ) -> RentalType:
        with transaction.atomic():
            user = info.context.request.user

            cart = await get_cart_by_id(cart_id)
            if not cart or not check_ownership(
                cart=cart,
                user_id=user.id,
                session_id=None,
            ):
                return None

            cart_items = await get_cart_items(cart.id)
            if not cart_items:
                return

            rented_due_date = datetime.now().date() + timedelta(days=30)
            delivery_type = DeliveryType(delivery_type.value)

            persist_items_prices(cart_items)

            rental = Rental.objects.create(
                cart_id=cart.id,
                user=user,
                rented_due_date=rented_due_date,
                delivery_type=delivery_type,
                address=address,
            )

            rental.save()

        return RentalType(
            id=rental.id,
            status=rental.status,
            total_price=rental.total_price,
            total_deposit=rental.total_deposit,
            rented_at=rental.rented_at.isoformat(),
            rented_due_date=rental.rented_due_date.isoformat(),
            returned_at=(
                rental.returned_at.isoformat() if rental.returned_at else None
            ),
            delivery_type=delivery_type,
            address=rental.address,
            cart=graphql_cart_mapper(pack_cart(cart.id, cart_items)),
        )

    @strawberry.mutation
    @login_required
    def cancel_rental(
        self,
        rental_id: int,
        info: strawberry.Info,
    ) -> bool:
        user = info.context.request.user
        rental = Rental.objects.filter(id=rental_id, user=user).first()

        if rental:
            rental.mark_as_cancelled()
            return True
        return False

    @strawberry.mutation
    @login_required
    def return_rental(
        self,
        rental_id: int,
        verification_photo_url: str,
        info: strawberry.Info,
    ) -> bool:
        user = info.context.request.user
        rental = Rental.objects.filter(id=rental_id, user=user).first()

        if rental:
            rental.mark_as_returned(verification_photo_url)
            return True
        else:
            raise PermissionDenied("You do not have permission to return this rental.")
