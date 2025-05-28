from typing import Any

from asyncio import iscoroutinefunction
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.backends import ModelBackend
from asgiref.sync import sync_to_async


class EmailBackend(ModelBackend):
    def authenticate(
        self,
        _: HttpRequest,
        email: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> AbstractUser | None:
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id: int) -> AbstractUser | None:
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


async def extract_user_identifier(
    request: HttpRequest,
) -> tuple[int | None, str | None]:
    user = await request.auser()

    if user and user.is_authenticated:
        return user.id, None

    if not request.session.session_key:
        await sync_to_async(request.session.create)()

    return None, request.session.session_key


def login_required(func):
    if iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            info = kwargs.get("info")
            if info is None:
                raise PermissionDenied("Missing context information.")

            user = await info.context.request.auser()
            if not user.is_authenticated:
                raise PermissionDenied("You must be logged in to perform this action.")

            return await func(*args, **kwargs)

    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            info = kwargs.get("info")
            if info is None:
                raise PermissionDenied("Missing context information.")

            user = info.context.request.user
            if not user.is_authenticated:
                raise PermissionDenied("You must be logged in to perform this action.")

            return func(*args, **kwargs)

    return wrapper
