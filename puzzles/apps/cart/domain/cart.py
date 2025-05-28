from functools import reduce
from decimal import Decimal
from typing import Iterable

from django.db.models import Q

from puzzles.apps.cart.models import Cart, CartItem
from puzzles.apps.catalog.models.puzzle import Puzzle, PuzzleStatus
from puzzles.apps.cart.domain import entity as cart_entity
from puzzles.common.numbers import stringify_price


def _get_user_filter_conditions(
    user_id: int | None, session_id: str | None
) -> Q | None:
    if user_id and session_id:
        return Q(user_id=user_id) | Q(session_id=session_id)
    elif user_id:
        return Q(user_id=user_id)
    elif session_id:
        return Q(session_id=session_id) & Q(user_id__isnull=True)

    return None


def get_cart_totals(cart_items: Iterable[CartItem]) -> tuple[Decimal, Decimal]:
    def reducer(
        amounts: tuple[Decimal, Decimal], cart_item: CartItem
    ) -> tuple[Decimal, Decimal]:
        price, deposit = amounts

        current_price = (
            cart_item.price if cart_item.price is not None else cart_item.item.price
        )
        current_deposit = (
            cart_item.deposit
            if cart_item.deposit is not None
            else cart_item.item.deposit
        )

        return price + current_price, deposit + current_deposit

    total_price, total_deposit = reduce(
        reducer,
        cart_items,
        (Decimal("0.0"), Decimal("0.0")),
    )

    return total_price, total_deposit


async def get_cart(user_id: int | None, session_id: str | None) -> Cart | None:
    user_conditions = _get_user_filter_conditions(user_id, session_id)
    if not user_conditions:
        return None
    try:
        cart = await Cart.objects.filter(user_conditions, rental__isnull=True).afirst()
    except Cart.DoesNotExist:
        return None
    return cart


async def get_or_create_cart(user_id: int | None, session_id: str | None) -> Cart:
    cart = await get_cart(user_id, session_id)
    if not cart:
        cart = Cart(
            user_id=user_id,
            session_id=session_id,
        )
        await cart.asave()

    return cart


async def get_cart_items(cart_id: int) -> list[CartItem]:
    existing_cart_items: list[CartItem] = []
    async for item in CartItem.objects.select_related("item").filter(cart_id=cart_id):
        existing_cart_items.append(item)

    return existing_cart_items


def pack_cart(cart_id: int, cart_items: Iterable[CartItem]) -> cart_entity.Cart:
    total_price, total_deposit = get_cart_totals(cart_items)

    return cart_entity.Cart(
        id=cart_id,
        items=tuple(
            cart_entity.CartItem(
                id=cart_item.id,
                puzzle_id=cart_item.item.id,
                title=cart_item.item.title,
                image_url=next(iter(cart_item.item.image_urls), None),
                price=stringify_price(
                    cart_item.price
                    if cart_item.price is not None
                    else cart_item.item.price
                ),
                deposit=stringify_price(
                    cart_item.deposit
                    if cart_item.deposit is not None
                    else cart_item.item.deposit
                ),
            )
            for cart_item in cart_items
        ),
        total_price=stringify_price(total_price),
        total_deposit=stringify_price(total_deposit),
    )


def check_ownership(cart: Cart, user_id: int | None, session_id: str | None) -> bool:
    return (cart.user_id is None and cart.session_id == session_id) or (
        cart.user_id is not None and cart.user_id == user_id
    )


async def add_item_to_cart(
    user_id: int | None, session_id: str | None, puzzle_id: int
) -> cart_entity.Cart | None:
    try:
        puzzle = await Puzzle.objects.filter(status=PuzzleStatus.ACTIVE).aget(
            pk=puzzle_id
        )
    except Puzzle.DoesNotExist:
        return None

    cart = await get_or_create_cart(user_id, session_id)
    existing_cart_items = await get_cart_items(cart.id)

    if any(puzzle_id == item.item.id for item in existing_cart_items):
        return None

    cart_item = CartItem(
        cart=cart,
        item=puzzle,
        price=puzzle.price,
        deposit=puzzle.deposit,
    )
    await cart_item.asave()

    cart_items = (cart_item, *existing_cart_items)

    return pack_cart(cart.id, cart_items)


async def remove_item_from_cart(
    user_id: int | None, session_id: str | None, item_id: int
) -> cart_entity.Cart | None:
    try:
        cart_item = await CartItem.objects.select_related("cart").aget(pk=item_id)
    except CartItem.DoesNotExist:
        return None

    cart = cart_item.cart
    if not check_ownership(cart=cart, user_id=user_id, session_id=session_id):
        return None

    await cart_item.adelete()

    cart_items = await get_cart_items(cart.id)
    if not cart_items:
        await cart.adelete()
        return None

    return pack_cart(cart.id, cart_items)


async def get_shopping_cart(
    user_id: int | None, session_id: str | None
) -> cart_entity.Cart | None:
    cart = await get_cart(user_id, session_id)
    if not cart:
        return None
    cart_items = await get_cart_items(cart.id)

    return pack_cart(cart.id, cart_items)


async def get_cart_by_id(cart_id: int) -> Cart | None:
    try:
        cart = await Cart.objects.aget(pk=cart_id)
    except Cart.DoesNotExist:
        return None
    return cart


async def bind_cart_to_user(user_id: int, session_id: str):
    if not session_id:
        return

    cart = await get_cart(user_id=None, session_id=session_id)
    if not cart:
        return

    cart.user_id = user_id
    cart.session_id = None
    await cart.asave()


async def persist_items_prices(cart_items: Iterable[CartItem]):
    for item in cart_items:
        item.price = item.item.price
        item.deposit = item.item.deposit

    await CartItem.objects.abulk_update(cart_items, ["price", "deposit"])
