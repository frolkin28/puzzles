import strawberry
from enum import Enum

from puzzles.cart.graph.types import Cart
from puzzles.rental.models.rental import DeliveryType


@strawberry.enum
class GraphQLEnumDeliveryType(Enum):
    NP = DeliveryType.NP.value
    UP = DeliveryType.UP.value
    PICKUP = DeliveryType.PICKUP.value
    COURIER = DeliveryType.COURIER.value


@strawberry.type
class RentalType:
    id: int
    status: int
    total_price: float
    total_deposit: float
    rented_at: str
    rented_due_date: str
    returned_at: str | None
    delivery_type: GraphQLEnumDeliveryType
    address: str
    cart: Cart
