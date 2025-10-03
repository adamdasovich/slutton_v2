from django.contrib import admin
from .models import GameCategory, Game, GameProgress, GameRating


@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty', 'play_count', 'average_rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_featured', 'is_active', 'requires_account']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['play_count', 'average_rating', 'created_at', 'updated_at']


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'completed', 'last_played', 'play_time_minutes']
    list_filter = ['completed', 'last_played']
    search_fields = ['user__username', 'game__name']
    readonly_fields = ['created_at', 'last_played']


@admin.register(GameRating)
class GameRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'game__name', 'review']
    readonly_fields = ['created_at', 'updated_at']
