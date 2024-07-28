import strawberry

from django.contrib.postgres.search import SearchQuery, SearchRank
from puzzles.catalog.models.puzzle import PuzzleStatus
from typing import Optional

from .types import PuzzleType, GraphQLEnumPuzzleCondition
from puzzles.catalog.models.puzzle import Puzzle


@strawberry.type
class CatalogQuery:
    @strawberry.field(description="Get all puzzles with optional filters")
    def all_puzzles(
        self,
        price_from: Optional[float] = None,
        price_to: Optional[float] = None,
        pieces_from: Optional[int] = None,
        pieces_to: Optional[int] = None,
        condition: Optional[GraphQLEnumPuzzleCondition] = None,
        search: Optional[str] = None,
        order_by: Optional[str] = None
    ) -> list[PuzzleType]:
        filters = {
            'status': PuzzleStatus.ACTIVE.value
        }
        if price_from is not None:
            filters['price__gte'] = price_from
        if price_to is not None:
            filters['price__lte'] = price_to
        if pieces_from is not None:
            filters['pieces__gte'] = pieces_from
        if pieces_to is not None:
            filters['pieces__lte'] = pieces_to
        if condition is not None:
            filters['condition'] = condition.value

        puzzles = Puzzle.objects.filter(**filters)

        if search:
            search = ' '.join(search.split())
            query = SearchQuery(search)
            puzzles = puzzles.annotate(
                rank=SearchRank('search_vector', query)
            ).filter(search_vector=query).order_by('-rank')

        if order_by:
            puzzles = puzzles.order_by(order_by)

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
