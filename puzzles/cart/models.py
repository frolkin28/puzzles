from django.db import models

from puzzles.catalog.models.puzzle import Puzzle
from puzzles.account.models import User


class Cart(models.Model):
    session_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.OneToOneField(Puzzle, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    verification_photo = models.URLField(max_length=1024, null=True)
