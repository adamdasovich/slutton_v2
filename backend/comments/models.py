from django.db import models
from django.conf import settings
from products.models import Product


class ProductComment(models.Model):
    """Product comment/discussion model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} on {self.product.name}: {self.content[:50]}"

    class Meta:
        verbose_name = "Product Comment"
        verbose_name_plural = "Product Comments"
        ordering = ['-created_at']
