from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.db.utils import IntegrityError


from puzzles.account.exc import UserAlreadyExists
from puzzles.account.models.user import User
from puzzles.account.schemas import RegisterModel


class EmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("Auth backend", email)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist as e:
            print(e)
            return None
        else:
            if user.check_password(password):
                print("check_password")
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


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
