from django.contrib.postgres.fields import ArrayField
from django.db import models
from puzzles.catalog.models.attribute import Attribute
from puzzles.catalog.models.puzzle_attribute import PuzzleAttribute
from enum import IntEnum, Enum

class PuzzleStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]

class PuzzleCondition(Enum):
    NEW = 'Новий'
    IDEAL = 'Ідеальний'
    VERY_GOOD = 'Дуже хороший'
    GOOD = 'Хороший'
    ALRIGHT = 'Задовільний'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]

class Puzzle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pieces = models.IntegerField()
    status = models.IntegerField(
        choices=PuzzleStatus.choices(),
        default=PuzzleStatus.ACTIVE.value
    )
    image_urls = ArrayField(
        models.URLField(max_length=1024), blank=True, default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    attributes = models.ManyToManyField(
        'Attribute', through='PuzzleAttribute'
    )
    condition = models.CharField(
        choices=PuzzleCondition.choices(),
    )

    def average_rating(self) -> float | None:
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None

    def average_difficulty(self) -> float | None:
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('difficulty'))['difficulty__avg']
        return None

    def __str__(self) -> str:
        return str(self.title)
