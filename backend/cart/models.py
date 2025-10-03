from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    """Shopping cart model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous Cart {self.session_key}"

    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Calculate total number of items in cart"""
        return sum(item.quantity for item in self.items.all())

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ['cart', 'product']
