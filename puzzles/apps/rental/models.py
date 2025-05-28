import datetime

from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone
from enum import IntEnum, unique

from asgiref.sync import sync_to_async
from puzzles.apps.account.models import User
from puzzles.apps.cart.models import Cart
from django.core.exceptions import ValidationError


@unique
class DeliveryType(IntEnum):
    NOVA_POSHTA = 1
    UKR_POSHTA = 2
    PICKUP = 3
    COURIER = 4

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]


@unique
class RentalStatus(IntEnum):
    RESERVED = 1
    ACTIVE = 2
    RETURNED = 3
    CANCELLED = 4

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]


class Rental(models.Model):
    MAX_RENTAL_DAYS = 30

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="rentals")
    cart = models.OneToOneField(
        Cart, on_delete=models.SET_NULL, related_name="rental", null=True, blank=True
    )
    status = models.SmallIntegerField(
        choices=RentalStatus.choices(), default=RentalStatus.RESERVED.value
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

    async def mark_as_returned(self, verification_photo_urls: list[str]):
        if self.status != RentalStatus.ACTIVE:
            raise PermissionDenied("Only rentals with status ACTIVE can be cancelled.")

        if len(verification_photo_urls) < 1 or len(verification_photo_urls) > 20:
            raise ValidationError("You should send at least 1 and maximum 20 photos")

        self.status = RentalStatus.RETURNED
        self.returned_at = timezone.now()

        await self.asave()

        photos = [
            VerificationPhoto(rental=self, url=url) for url in verification_photo_urls
        ]
        await sync_to_async(VerificationPhoto.objects.bulk_create)(photos)

    async def mark_as_cancelled(self) -> None:
        if self.status != RentalStatus.RESERVED:
            raise PermissionDenied(
                "Only rentals with status RESERVED can be cancelled."
            )
        self.status = RentalStatus.CANCELLED
        await self.asave()

    def __str__(self) -> str:
        return f"{self.id} - {self.user.email}"

    @classmethod
    def get_rented_due_date(cls) -> datetime.date:
        return datetime.datetime.now().date() + datetime.timedelta(
            days=cls.MAX_RENTAL_DAYS
        )


class VerificationPhoto(models.Model):
    rental = models.ForeignKey(
        Rental, related_name="verification_photos", on_delete=models.CASCADE
    )
    url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        default=None,
    )
