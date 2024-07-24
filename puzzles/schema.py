import strawberry
from strawberry.extensions import QueryDepthLimiter
from puzzles.catalog.graph.query import CatalogQuery

MAX_DEPTH = 10


@strawberry.type
class Query:
    catalog: CatalogQuery


schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryDepthLimiter(
            max_depth=MAX_DEPTH,
            callback=lambda depth: print(f"Depth limit reached: {depth}")
        ),
    ],
)
