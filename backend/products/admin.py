from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVideo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'category', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVideoInline]
    readonly_fields = ['created_at', 'updated_at']
