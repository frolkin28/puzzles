from django.db import models
from django.utils import timezone
from enum import IntEnum

from puzzles.account.models.user import User


class DeliveryType(IntEnum):
    NP = 1
    UP = 2
    PICKUP = 3
    COURIER = 4

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]


class RentalStatus(IntEnum):
    RESERVED = 1
    ACTIVE = 2
    RETURNED = 3
    CANCELLED = 4

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]


class Rental(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='rentals'
    )
    status = models.IntegerField(
        choices=RentalStatus.choices(),
        default=RentalStatus.RESERVED.value
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    total_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    rented_at = models.DateTimeField(auto_now_add=True)
    rented_due_date = models.DateField()
    returned_at = models.DateTimeField(blank=True, null=True)
    delivery_type = models.IntegerField(
        choices=DeliveryType.choices(),
    )
    address = models.TextField(blank=True, null=True)

    def is_reserved(self) -> bool:
        return self.status == RentalStatus.RESERVED

    def is_active(self) -> bool:
        return self.status == RentalStatus.ACTIVE

    def is_returned(self) -> bool:
        return self.status == RentalStatus.RETURNED

    def mark_as_active(self) -> None:
        self.status = RentalStatus.ACTIVE
        self.rented_at = timezone.now()
        self.save()

    def mark_as_returned(self) -> None:
        self.status = RentalStatus.RETURNED
        self.returned = True
        self.returned_at = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.puzzle.title}'

