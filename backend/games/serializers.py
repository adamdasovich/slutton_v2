from rest_framework import serializers
from .models import GameCategory, Game, GameProgress, GameRating


class GameCategorySerializer(serializers.ModelSerializer):
    """Game category serializer"""
    game_count = serializers.SerializerMethodField()

    class Meta:
        model = GameCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'game_count', 'created_at']

    def get_game_count(self, obj):
        return obj.games.filter(is_active=True).count()


class GameSerializer(serializers.ModelSerializer):
    """Game serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    preview_gif_url = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'category', 'category_name', 'game_url', 'thumbnail_url', 'preview_gif_url',
            'difficulty', 'play_count', 'average_rating', 'duration_minutes',
            'is_featured', 'requires_account', 'created_at', 'updated_at'
        ]

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None

    def get_preview_gif_url(self, obj):
        if obj.preview_gif:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview_gif.url)
        return None


class GameProgressSerializer(serializers.ModelSerializer):
    """Game progress serializer"""
    game_name = serializers.CharField(source='game.name', read_only=True)

    class Meta:
        model = GameProgress
        fields = ['id', 'game', 'game_name', 'progress_data', 'completed', 'last_played', 'play_time_minutes', 'created_at']
        read_only_fields = ['created_at']


class GameRatingSerializer(serializers.ModelSerializer):
    """Game rating serializer"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = GameRating
        fields = ['id', 'user', 'username', 'game', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
