import strawberry
from strawberry import Info

from puzzles.account.lib import login_required
from puzzles.account.models import User
from puzzles.review.graph.types import ReviewType
from puzzles.review.models import Review


@strawberry.type
class ReviewMutation:
    @strawberry.mutation(description="Add a review for a puzzle")
    @login_required
    def add_review(
        self,
        user_id: int,
        puzzle_id: int,
        condition: int,
        rating: int,
        difficulty: int,
        info: Info,
    ) -> ReviewType:
        review = Review.objects.create(
            user_id=user_id,
            puzzle_id=puzzle_id,
            condition=condition,
            rating=rating,
            difficulty=difficulty,
        )
        return ReviewType.from_model(review)
