from django.contrib import admin
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
