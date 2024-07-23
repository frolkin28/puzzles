from enum import IntEnum

from django.db import models
from django.urls import reverse


class DeliveryType(IntEnum):
    NP = 1
    UP = 2
    PICKUP = 3
    COURIER = 4

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]


class Puzzle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pieces = models.IntegerField()
    # image = models.ImageField(upload_to='puzzles/')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_type = models.IntegerField(
        choices=DeliveryType.choices(),
    )
    tags = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('puzzles:detail', kwargs={'id': self.pk})

    def average_rating(self) -> float | None:
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None

    def average_difficulty(self) -> float | None:
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('difficulty'))[
                'difficulty__avg']
        return None

    def __str__(self) -> str:
        return str(self.title)
