from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("session_id", "user", "user_id", "date_created")
    search_fields = ("token", "user__username", "user__id")
    list_filter = ("date_created",)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "item", "price", "deposit", "verification_photo")
    search_fields = ("cart__token", "item__name", "item__id")
    list_filter = ("cart__date_created",)
