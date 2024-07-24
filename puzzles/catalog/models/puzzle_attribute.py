from django.db import models

class PuzzleAttribute(models.Model):
    puzzle = models.ForeignKey('Puzzle', on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.puzzle.title} - '
                f'{self.attribute.name}: {self.attribute.value}')
