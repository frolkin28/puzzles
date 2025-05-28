import strawberry
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from puzzles.common.auth import login_required
from puzzles.apps.review.graph.types import ReviewType
from puzzles.apps.review.models import Review


@strawberry.type(name="Mutation", extend=True)
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
    ) -> ReviewType:
        review = Review.objects.create(
            user_id=user_id,
            puzzle_id=puzzle_id,
            condition=condition,
            rating=rating,
            difficulty=difficulty,
        )
        return ReviewType.from_model(review)

    @strawberry.mutation(description="Update a review for a puzzle")
    @login_required
    async def update_review(
        self,
        review_id: int,
        condition: int | None = None,
        rating: int | None = None,
        difficulty: int | None = None,
    ) -> ReviewType:
        try:
            review = Review.objects.get(id=review_id)
            if timezone.now() - review.created_at > timedelta(hours=24):
                raise Exception(
                    "You can only update a review within 24 hours of creation"
                )

            if condition is not None:
                review.condition = condition
            if rating is not None:
                review.rating = rating
            if difficulty is not None:
                review.difficulty = difficulty
            await review.asave()
            return ReviewType.from_model(review)
        except Review.DoesNotExist:
            raise ObjectDoesNotExist("Not found puzzle")
