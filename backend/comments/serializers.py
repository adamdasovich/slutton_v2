from rest_framework import serializers
from .models import ProductComment


class ProductCommentSerializer(serializers.ModelSerializer):
    """Product comment serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = ['id', 'user_id', 'username', 'content', 'parent_comment', 'is_edited',
                  'replies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'user_id', 'is_edited', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return ProductCommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []
