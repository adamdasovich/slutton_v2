"""
Script to generate all admin files
"""

USERS_ADMIN = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'age_verified', 'date_of_birth', 'is_staff']
    list_filter = ['age_verified', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age_verified', 'date_of_birth', 'phone_number')}),
    )
"""

PRODUCTS_ADMIN = """from django.contrib import admin
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
"""

CART_ADMIN = """from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'total_price', 'created_at']
    readonly_fields = ['total_price', 'total_items', 'created_at', 'updated_at']
    inlines = [CartItemInline]
"""

ORDERS_ADMIN = """from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status', 'total_amount', 'stripe_payment_intent_id')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address_line1', 'shipping_address_line2', 'shipping_city',
                      'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Billing Address', {
            'fields': ('billing_address_line1', 'billing_address_line2', 'billing_city',
                      'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
"""

RATINGS_ADMIN = """from django.contrib import admin
from .models import ProductRating


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
"""

COMMENTS_ADMIN = """from django.contrib import admin
from .models import ProductComment


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'content_preview', 'parent_comment', 'created_at']
    list_filter = ['created_at', 'is_edited']
    search_fields = ['user__username', 'product__name', 'content']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
"""

# Write all admin files
with open('users/admin.py', 'w') as f:
    f.write(USERS_ADMIN)

with open('products/admin.py', 'w') as f:
    f.write(PRODUCTS_ADMIN)

with open('cart/admin.py', 'w') as f:
    f.write(CART_ADMIN)

with open('orders/admin.py', 'w') as f:
    f.write(ORDERS_ADMIN)

with open('ratings/admin.py', 'w') as f:
    f.write(RATINGS_ADMIN)

with open('comments/admin.py', 'w') as f:
    f.write(COMMENTS_ADMIN)

print("All admin files generated successfully!")
