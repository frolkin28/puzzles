from enum import IntEnum

from django.db import models
from django.utils import timezone

from puzzles.puzzles.models.puzzle import Puzzle
from puzzles.puzzles.models.user import User


class BookingStatus(IntEnum):
    PENDING = 1
    APPROVED = 2
    CANCELLED = 3

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(key.value, key.name.capitalize()) for key in cls]
    

class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='booking'
    )
    puzzle = models.ForeignKey(
        Puzzle, on_delete=models.CASCADE,
        related_name='booking'
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=BookingStatus.choices(),
        default=BookingStatus.PENDING.value
    )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.puzzle.title} (Booked)'
