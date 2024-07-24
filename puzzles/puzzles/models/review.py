from django.db import models

from puzzles.puzzles.models.puzzle import Puzzle
from puzzles.puzzles.models.user import User


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    puzzle = models.ForeignKey(
        Puzzle, on_delete=models.CASCADE, related_name='reviews'
    )
    condition = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    difficulty = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.puzzle.title}'

    class Meta:
        ordering = ['-created_at']
