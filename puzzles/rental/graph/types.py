import strawberry
from typing import List


@strawberry.type
class RentalItemType:
    puzzle_id: int
    price: float
    deposit: float


@strawberry.type
class RentalType:
    id: int
    status: int
    total_price: float
    total_deposit: float
    rented_at: str
    rented_due_date: str
    returned_at: str
    delivery_type: int
    address: str


@strawberry.input
class RentalItemInput:
    puzzle_id: int
    price: float
    deposit: float


@strawberry.input
class CreateRentalInput:
    user_id: int
    rented_due_date: str
    delivery_type: int
    address: str
    items: List[RentalItemInput]


@strawberry.type
class RentalItemTypeOutput:
    id: int
    rental_id: int
    puzzle_id: int
    price: float
    deposit: float
    verification_photo: str


@strawberry.type
class CreateRentalOutput:
    rental: RentalType
    items: List[RentalItemTypeOutput]
