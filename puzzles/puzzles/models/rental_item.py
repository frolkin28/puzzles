from django.db import models

from puzzles.puzzles.models.puzzle import Puzzle
from puzzles.puzzles.models.rental import Rental


class RentalItem(models.Model):
    rental = models.ForeignKey(
        Rental, on_delete=models.CASCADE,
        related_name='rental_items'
    )
    puzzle = models.ForeignKey(
        Puzzle, on_delete=models.CASCADE,
        related_name='rental_items'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    verification_photo = models.URLField(max_length=1024)
