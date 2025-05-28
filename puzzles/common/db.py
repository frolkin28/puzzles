from typing import TypeVar, Self

from asgiref.sync import sync_to_async
from django.db.transaction import Atomic
from django.db.models.manager import BaseManager


TModel = TypeVar("TModel")


class AsyncAtomicContextManager(Atomic):
    def __init__(self, using=None, savepoint=True, durable=False):
        super().__init__(using, savepoint, durable)

    async def __aenter__(self) -> Self:
        await sync_to_async(super().__enter__)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await sync_to_async(super().__exit__)(exc_type, exc_value, traceback)


async def iterate_queryset(queryset: BaseManager[TModel]) -> list[TModel]:
    res = []
    async for entry in queryset.aiterator():
        res.append(entry)
    return res
