import strawberry
from enum import Enum

from puzzles.apps.cart.graph.types import Cart
from puzzles.apps.rental.models import DeliveryType


@strawberry.enum
class GraphQLEnumDeliveryType(Enum):
    NOVA_POSHTA = DeliveryType.NOVA_POSHTA.value
    UKR_POSHTA = DeliveryType.UKR_POSHTA.value
    PICKUP = DeliveryType.PICKUP.value
    COURIER = DeliveryType.COURIER.value


@strawberry.type
class Rental:
    id: int
    status: int
    total_price: str
    total_deposit: str
    rented_at: str
    rented_due_date: str
    returned_at: str | None
    delivery_type: GraphQLEnumDeliveryType
    address: str | None
    cart: Cart | None
