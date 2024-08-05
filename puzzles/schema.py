from puzzles.cart.graph.query import CartQuery
import strawberry
from strawberry.extensions import QueryDepthLimiter

from puzzles.catalog.graph.query import CatalogQuery
from puzzles.rental.graph.mutation import RentalMutation
from puzzles.rental.graph.query import RentalQuery
from puzzles.cart.graph.mutation import CartMutation


MAX_DEPTH = 10


@strawberry.type
class Query(CartQuery):
    catalog: CatalogQuery = strawberry.field(resolver=lambda: CatalogQuery())
    rental: RentalQuery = strawberry.field(resolver=lambda: RentalQuery())


@strawberry.type
class Mutation(CartMutation):
    rental: RentalMutation = strawberry.field(resolver=lambda: RentalMutation())


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(
            max_depth=MAX_DEPTH,
            callback=lambda depth: print(f"Depth limit reached: {depth}"),
        ),
    ],
)
