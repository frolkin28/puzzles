import strawberry
from .types import PuzzleType
from puzzles.catalog.models.puzzle import Puzzle


@strawberry.type
class CatalogQuery:
    @strawberry.field(description="Get all puzzles in the catalog")
    def all_puzzles(self) -> list[PuzzleType]:
        puzzles = Puzzle.objects.all()
        return [
            PuzzleType(
                id=puzzle.id,
                title=puzzle.title,
                description=puzzle.description,
                pieces=puzzle.pieces,
                status=puzzle.status,
                image_urls=puzzle.image_urls,
                created_at=puzzle.created_at.isoformat(),
                price=puzzle.price,
                deposit=puzzle.deposit,
                condition=puzzle.condition,
                attributes=[attr.name for attr in puzzle.attributes.all()]
            ) for puzzle in puzzles
        ]
