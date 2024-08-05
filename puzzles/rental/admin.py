from django.contrib import admin

from puzzles.rental.models.rental import Rental
from puzzles.rental.models.rental_item import RentalItem


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'status', 'total_price', 'total_deposit', 'rented_at', 'rented_due_date', 'returned_at', 'delivery_type', 'address'
    )
    readonly_fields = (
        'total_price', 'total_deposit', 'rented_at', 'returned_at'
    )


@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = (
        'rental', 'puzzle', 'price', 'deposit', 'verification_photo'
    )
    readonly_fields = (
        'price', 'deposit'
    )
