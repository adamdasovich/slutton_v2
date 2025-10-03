from rest_framework import serializers
from .models import ProductRating


class ProductRatingSerializer(serializers.ModelSerializer):
    """Product rating serializer"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProductRating
        fields = ['id', 'username', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
