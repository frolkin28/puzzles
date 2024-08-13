import strawberry
from typing import Optional
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.exceptions import ObjectDoesNotExist

from puzzles.catalog.models.puzzle import PuzzleStatus
from puzzles.catalog.models.puzzle import Puzzle
from .types import PuzzleType, GraphQLEnumPuzzleCondition


@strawberry.type
class CatalogQuery:
    @strawberry.field(description="Get puzzles with optional filters")
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
            PuzzleType.from_model(puzzle) for puzzle in puzzles
        ]

    @strawberry.field(description="Get puzzle by ID")
    def puzzle_by_id(self, pizzle_id: int) -> Optional[PuzzleType]:
        try:
            puzzle = Puzzle.objects.get(id=pizzle_id)
            return PuzzleType.from_model(puzzle)
        except Puzzle.DoesNotExist:
            raise ObjectDoesNotExist("Not found puzzle")
