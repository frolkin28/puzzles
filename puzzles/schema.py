import strawberry
from strawberry.extensions import QueryDepthLimiter

from puzzles.apps.cart.graph.query import CartQuery
from puzzles.apps.catalog.graph.query import CatalogQuery
from puzzles.apps.rental.graph.mutation import RentalMutation
from puzzles.apps.rental.graph.query import RentalQuery
from puzzles.apps.review.graph.mutation import ReviewMutation
from puzzles.apps.review.graph.query import ReviewQuery
from puzzles.apps.cart.graph.mutation import CartMutation


MAX_DEPTH = 10


@strawberry.type
class Query(
    CartQuery,
    CatalogQuery,
    RentalQuery,
    ReviewQuery,
):
    pass


@strawberry.type
class Mutation(
    CartMutation,
    RentalMutation,
    ReviewMutation,
):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(
            max_depth=MAX_DEPTH,
        ),
    ],
)
