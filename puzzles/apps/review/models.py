from django.db import models

from puzzles.apps.catalog.models.puzzle import Puzzle
from puzzles.apps.account.models import User


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='reviews'
    )
    puzzle = models.ForeignKey(
        Puzzle, on_delete=models.CASCADE, related_name='reviews'
    )
    condition = models.PositiveSmallIntegerField()
    rating = models.PositiveSmallIntegerField()
    difficulty = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.puzzle.title}'

    class Meta:
        ordering = ['-created_at']
