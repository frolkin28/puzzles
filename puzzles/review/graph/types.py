import strawberry

from puzzles.review.models import Review


@strawberry.type(description="Type represents a review for a puzzle.")
class ReviewType:
    id: int = strawberry.field(description="The internal review id.")
    user: str = strawberry.field(description="Username of the reviewer.")
    condition: int = strawberry.field(description="Condition rating of the puzzle.")
    rating: int = strawberry.field(description="Rating given by the user.")
    difficulty: int = strawberry.field(description="Difficulty rating of the puzzle.")
    created_at: str = strawberry.field(description="Creation date of the review.")

    @staticmethod
    def from_model(model: Review) -> "ReviewType":
        return ReviewType(
            id=model.id,
            user=model.user.first_name,
            condition=model.condition,
            rating=model.rating,
            difficulty=model.difficulty,
            created_at=model.created_at.isoformat(),
        )
