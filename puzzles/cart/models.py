from django.db import models

from puzzles.catalog.models.puzzle import Puzzle


class Cart(models.Model):
    token = models.CharField(max_length=36, unique=True, blank=True, null=True)

    # user_id
    # date_created


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    # item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    verification_photo = models.URLField(max_length=1024)
    
