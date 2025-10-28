from django.contrib import admin
from django.contrib import messages
from django import forms
from .models import GameCategory, Game, GameProgress, GameRating, DailyMemoryImages
from .claude_image_service import ClaudeImageGenerator


class GameAdminForm(forms.ModelForm):
    """Custom form to allow relative paths in game_url"""
    game_url = forms.CharField(
        max_length=500,
        help_text="URL or path to the game (e.g., /games/ouija or https://example.com)"
    )

    class Meta:
        model = Game
        fields = '__all__'


@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm
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


@admin.register(DailyMemoryImages)
class DailyMemoryImagesAdmin(admin.ModelAdmin):
    list_display = ['date', 'theme', 'is_active', 'image_count', 'created_at']
    list_filter = ['is_active', 'date']
    search_fields = ['theme', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    actions = ['regenerate_images']

    def image_count(self, obj):
        """Display number of images"""
        return len(obj.images)
    image_count.short_description = 'Images'

    def regenerate_images(self, request, queryset):
        """Regenerate images using Claude AI"""
        generator = ClaudeImageGenerator()
        success_count = 0

        for daily_images in queryset:
            try:
                # Generate new images
                image_data = generator.generate_daily_images(daily_images.date)

                # Update existing record
                daily_images.theme = image_data['theme']
                daily_images.description = image_data['description']
                daily_images.images = image_data['images']
                daily_images.save()

                success_count += 1

            except Exception as e:
                self.message_user(
                    request,
                    f'Error regenerating images for {daily_images.date}: {str(e)}',
                    level=messages.ERROR
                )

        if success_count > 0:
            self.message_user(
                request,
                f'Successfully regenerated images for {success_count} date(s)',
                level=messages.SUCCESS
            )

    regenerate_images.short_description = 'Regenerate images with Claude AI'
