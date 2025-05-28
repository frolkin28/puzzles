from typing import Any

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields: Any) -> "User":
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(blank=False, max_length=150, null=False)
    last_name = models.CharField(blank=False, max_length=150, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_subscriber = models.BooleanField(blank=False, default=False)
    subscription_expiration = models.DateField(blank=True, null=True)
    contacts = models.CharField(max_length=256, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
