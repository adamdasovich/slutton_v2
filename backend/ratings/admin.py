from django.contrib import admin
from .models import ProductRating


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
