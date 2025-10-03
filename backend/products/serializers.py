from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVideo


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'product_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Product image serializer"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'order']


class ProductVideoSerializer(serializers.ModelSerializer):
    """Product video serializer"""
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductVideo
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail', 'duration', 'file_size', 'download_url', 'created_at']

    def get_download_url(self, obj):
        # In production, this would generate a signed URL from S3
        request = self.context.get('request')
        if request and obj.video_file:
            return request.build_absolute_uri(obj.video_file.url)
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Product list serializer (lightweight)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    rating_count = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'category_name',
                  'stock_quantity', 'primary_image', 'average_rating', 'rating_count', 'created_at']

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            return request.build_absolute_uri(primary.image.url) if request else primary.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Product detail serializer (full details)"""
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    rating_count = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'category', 'stock_quantity',
                  'sku', 'is_active', 'images', 'videos', 'average_rating', 'rating_count',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
