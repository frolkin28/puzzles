import strawberry
from datetime import datetime
from django.db import transaction

from puzzles.account.models.user import User
from puzzles.catalog.models.puzzle import Puzzle
from puzzles.rental.graph.types import RentalType, CreateRentalInput, \
    CreateRentalOutput, RentalItemTypeOutput
from puzzles.rental.models.rental import Rental
from puzzles.rental.models.rental_item import RentalItem


@strawberry.type
class RentalMutation:
    @strawberry.mutation
    def create_rental(self, input: CreateRentalInput) -> CreateRentalOutput:
        with transaction.atomic():
            user = User.objects.get(pk=input.user_id)
            rental = Rental.objects.create(
                user=user,
                rented_due_date=datetime.strptime(input.rented_due_date, '%Y-%m-%d').date(),
                delivery_type=input.delivery_type,
                address=input.address
            )

            total_price = 0
            total_deposit = 0

            rental_items_output = []

            for item in input.items:
                puzzle = Puzzle.objects.get(pk=item.puzzle_id)
                rental_item = RentalItem.objects.create(
                    rental=rental,
                    puzzle=puzzle,
                    price=item.price,
                    deposit=item.deposit,
                    verification_photo=""
                )
                total_price += item.price
                total_deposit += item.deposit

                rental_items_output.append(RentalItemTypeOutput(
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

        rental_output = RentalType(
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
            delivery_type=rental.delivery_type,
            address=rental.address
        )

        return CreateRentalOutput(
            rental=rental_output,
            items=rental_items_output
        )
