from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .schemas import CustomUserCreationForm, CustomUserChangeForm
from puzzles.account.models.user import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone_number", "contacts")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
        ("Subscription", {"fields": ("is_subscriber", "subscription_expiration")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_subscriber",
                    "subscription_expiration",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff", "is_subscriber")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
