from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product


class ProductRating(models.Model):
    """Product rating model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.rating} stars"

    class Meta:
        verbose_name = "Product Rating"
        verbose_name_plural = "Product Ratings"
        unique_together = ['user', 'product']  # One rating per user per product
        ordering = ['-created_at']
