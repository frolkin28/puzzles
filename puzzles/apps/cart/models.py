from decimal import Decimal

from django.db import models

from puzzles.apps.catalog.models.puzzle import Puzzle
from puzzles.apps.account.models import User


class Cart(models.Model):
    session_id = models.CharField(max_length=255, blank=True, null=True, unique=False)

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="carts")
    date_created = models.DateTimeField(auto_now_add=True, null=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Puzzle, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
