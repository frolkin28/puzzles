import datetime

from puzzles.apps.rental.models import Rental


MAX_RENTAL_DAYS = 30


async def is_cart_already_rented(cart_id: int) -> bool:
    try:
        await Rental.objects.aget(cart_id=cart_id)
    except Rental.DoesNotExist:
        return False

    return True
