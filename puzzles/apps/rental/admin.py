from django.contrib import admin

from puzzles.apps.rental.models import Rental, VerificationPhoto


class VerificationPhotoInline(admin.TabularInline):
    model = VerificationPhoto
    extra = 0


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    inlines = [VerificationPhotoInline]
    list_display = (
        "id",
        "user",
        "status",
        "rented_at",
        "rented_due_date",
        "returned_at",
        "delivery_type",
    )
    readonly_fields = ("rented_at", "returned_at")


@admin.register(VerificationPhoto)
class VerificationPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "rental", "url")
    search_fields = (
        "id",
        "url",
    )
    list_filter = ("rental",)
