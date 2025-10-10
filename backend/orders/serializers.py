from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer"""
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'product_name', 'product_sku', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer"""
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user_email', 'status', 'total_amount', 'items', 'items_count',
                  'shipping_address_line1', 'shipping_address_line2', 'shipping_city',
                  'shipping_state', 'shipping_postal_code', 'shipping_country',
                  'billing_address_line1', 'billing_address_line2', 'billing_city',
                  'billing_state', 'billing_postal_code', 'billing_country',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        return obj.items.count()


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating orders"""
    shipping_address_line1 = serializers.CharField(max_length=255)
    shipping_address_line2 = serializers.CharField(max_length=255, allow_blank=True, required=False)
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=100)
    shipping_postal_code = serializers.CharField(max_length=20)
    shipping_country = serializers.CharField(max_length=100, default='US')

    billing_same_as_shipping = serializers.BooleanField(default=True)
    billing_address_line1 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    billing_address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    billing_city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    billing_state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    billing_postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    billing_country = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs.get('billing_same_as_shipping'):
            required_fields = ['billing_address_line1', 'billing_city', 'billing_state', 'billing_postal_code']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required when billing address is different.")
        return attrs
