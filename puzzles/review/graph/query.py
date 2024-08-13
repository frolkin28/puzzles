import strawberry
from django.core.exceptions import ObjectDoesNotExist

from puzzles.catalog.models import Puzzle
from puzzles.review.graph.types import ReviewType


@strawberry.type
class ReviewQuery:
    @strawberry.field(description="Get reviews with optional filters")
    def reviews_by_puzzle(self, puzzle_id: int) -> list[ReviewType]:
        try:
            puzzle = Puzzle.objects.get(pk=puzzle_id)
            return [ReviewType.from_model(review) for review in
                    puzzle.reviews.all()]
        except Puzzle.DoesNotExist:
            raise ObjectDoesNotExist("Not found puzzle")
