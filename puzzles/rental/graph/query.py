import strawberry

from puzzles.rental.graph.types import RentalType, GraphQLEnumDeliveryType, \
    RentalItemType
from puzzles.rental.models import Rental, RentalItem


@strawberry.type
class RentalQuery:
    @strawberry.field(description="Get rentals with optional filters")
    def rentals(
        self,
        info,
        is_for_user: bool = False,
    ) -> list[RentalType]:
        user = info.context.request.user

        if is_for_user:
            if not user.is_authenticated:
                raise Exception("User not authenticated")
            rentals = Rental.objects.filter(user=user)
        else:
            rentals = Rental.objects.all()

        rental_items = RentalItem.objects.filter(rental__in=rentals)
        rental_items_by_rental = {rental.id: [] for rental in rentals}
        for item in rental_items:
            rental_items_by_rental[item.rental.id].append(RentalItemType(
                id=item.id,
                rental_id=item.rental.id,
                puzzle_id=item.puzzle.id,
                price=item.price,
                deposit=item.deposit,
                verification_photo=item.verification_photo
            ))

        return [
            RentalType(
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
                delivery_type=GraphQLEnumDeliveryType(rental.delivery_type),
                address=rental.address,
                items=rental_items_by_rental[rental.id]
            )
            for rental in rentals
        ]
