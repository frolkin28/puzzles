import strawberry
from datetime import datetime, timedelta
from django.db import transaction

from puzzles.catalog.models.puzzle import Puzzle
from puzzles.rental.graph.types import (
    RentalType, GraphQLEnumDeliveryType, RentalItemType
)
from puzzles.rental.models.rental import Rental, DeliveryType
from puzzles.rental.models.rental_item import RentalItem


@strawberry.type
class RentalMutation:
    @strawberry.mutation
    def create_rental(
        self,
        delivery_type: GraphQLEnumDeliveryType,
        address: str,
        puzzle_ids: list[int],
        info
    ) -> RentalType:
        with transaction.atomic():

            user = info.context.request.user
            if not user.is_authenticated:
                raise Exception("User not authenticated")

            rented_due_date = datetime.now().date() + timedelta(days=30)
            delivery_type = DeliveryType(delivery_type.value)

            rental = Rental.objects.create(
                user=user,
                rented_due_date=rented_due_date,
                delivery_type=delivery_type,
                address=address
            )

            total_price = 0
            total_deposit = 0

            rental_items_output = []

            for puzzle_id in puzzle_ids:
                puzzle = Puzzle.objects.get(pk=puzzle_id)
                rental_item = RentalItem.objects.create(
                    rental=rental,
                    puzzle=puzzle,
                    price=puzzle.price,
                    deposit=puzzle.deposit,
                    verification_photo=""
                )
                total_price += puzzle.price
                total_deposit += puzzle.deposit

                rental_items_output.append(RentalItemType(
                    id=rental_item.id,
                    rental_id=rental_item.rental.id,
                    puzzle_id=rental_item.puzzle.id,
                    price=rental_item.price,
                    deposit=rental_item.deposit,
                    verification_photo=rental_item.verification_photo
                ))

            rental.total_price = total_price
            rental.total_deposit = total_deposit
            rental.save()

        return RentalType(
            id=rental.id,
            status=rental.status,
            total_price=rental.total_price,
            total_deposit=rental.total_deposit,
            rented_at=rental.rented_at.isoformat(),
            rented_due_date=rental.rented_due_date.isoformat(),
            returned_at=(
                rental.returned_at.isoformat()
                if rental.returned_at
                else None
            ),
            delivery_type=delivery_type,
            address=rental.address,
            items=rental_items_output
        )
