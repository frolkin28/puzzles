from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from puzzles.account.models.user import User

from pydantic import BaseModel, Field


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class RegisterModel(BaseModel):
    email: str = Field(max_length=254)
    first_name: str = Field(min_length=2, max_length=150)
    last_name: str = Field(min_length=2, max_length=150)
    password: str = Field(min_length=8, max_length=128)
    contacts: str | None = Field(default=None)


class LoginModel(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)
