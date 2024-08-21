from typing import TypeVar

from django.db.models.manager import BaseManager


TModel = TypeVar("TModel")


async def iterate_queryset(queryset: BaseManager[TModel]) -> list[TModel]:
    res = []
    async for entry in queryset.aiterator():
        res.append(entry)
    return res
