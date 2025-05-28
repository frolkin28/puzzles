from django.db.utils import IntegrityError

from puzzles.apps.account.domain.exc import UserAlreadyExists
from puzzles.apps.account.models import User
from puzzles.apps.account.schemas import RegisterModel


def register_user(payload: RegisterModel) -> User:
    """
    Raises: UserAlreadyExists
    """

    try:
        user = User.objects.create_user(
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            contacts=payload.contacts,
        )
    except IntegrityError as e:
        raise UserAlreadyExists from e
    return user
