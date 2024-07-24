import strawberry

from puzzles.catalog.models.attribute import Attribute
from puzzles.catalog.models.puzzle import Puzzle


@strawberry.type(description="Type represents a puzzle.")
class PuzzleType:
    id: int = strawberry.field(description="The internal puzzle id.")
    title: str = strawberry.field(description="Title of the puzzle.")
    description: str = strawberry.field(description="Description of the puzzle.")
    pieces: int = strawberry.field(description="Number of pieces in the puzzle.")
    status: int = strawberry.field(description="Status of the puzzle.")
    image_urls: list[str] = strawberry.field(description="URLs of puzzle images.")
    created_at: str = strawberry.field(description="Creation date of the puzzle.")
    price: float = strawberry.field(description="Price of the puzzle.")
    deposit: float = strawberry.field(description="Deposit for the puzzle.")
    condition: str = strawberry.field(description="Condition of the puzzle.")
    attributes: list['AttributeType'] = strawberry.field(description="Attributes associated with the puzzle.")

    @staticmethod
    def from_model(model: Puzzle) -> "PuzzleType":
        return PuzzleType(
            id=model.id,
            title=model.title,
            description=model.description,
            pieces=model.pieces,
            status=model.status,
            image_urls=model.image_urls,
            created_at=model.created_at.isoformat(),
            price=model.price,
            deposit=model.deposit,
            condition=model.condition,
            attributes=[AttributeType.from_model(attr) for attr in model.attributes.all()]
        )


@strawberry.type(description="Type represents an attribute for a puzzle.")
class AttributeType:
    id: int = strawberry.field(description="The internal attribute id.")
    name: str = strawberry.field(description="Name of the attribute.")

    @staticmethod
    def from_model(model: Attribute) -> "AttributeType":
        return AttributeType(
            id=model.id,
            name=model.name,
        )
