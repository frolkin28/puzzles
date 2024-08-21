from django.contrib import admin

from puzzles.rental.models.rental import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "total_price",
        "total_deposit",
        "rented_at",
        "rented_due_date",
        "returned_at",
        "delivery_type",
        "address",
    )
    readonly_fields = ("total_price", "total_deposit", "rented_at", "returned_at")
