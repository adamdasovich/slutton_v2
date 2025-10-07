from django.db import models
from django.utils.text import slugify
from users.models import CustomUser


class GameCategory(models.Model):
    """Game category model"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Game Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Game(models.Model):
    """Game model"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Teaser description")
    category = models.ForeignKey(GameCategory, on_delete=models.SET_NULL, null=True, related_name='games')

    # Game content
    game_url = models.URLField(help_text="URL to the game (iframe source)")
    thumbnail = models.ImageField(upload_to='games/thumbnails/', blank=True, null=True)
    preview_gif = models.ImageField(upload_to='games/previews/', blank=True, null=True, help_text="Animated preview")

    # Metadata
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    play_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    duration_minutes = models.PositiveIntegerField(default=15, help_text="Average playtime in minutes")

    # Features
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    requires_account = models.BooleanField(default=False)
    age_restricted = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-play_count', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def increment_play_count(self):
        """Increment play count"""
        self.play_count += 1
        self.save(update_fields=['play_count'])


class GameProgress(models.Model):
    """Track user progress in games"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='game_progress')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='user_progress')

    # Progress data
    progress_data = models.JSONField(default=dict, blank=True, help_text="Game-specific progress data")
    completed = models.BooleanField(default=False)
    last_played = models.DateTimeField(auto_now=True)
    play_time_minutes = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'game']
        ordering = ['-last_played']

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"


class GameRating(models.Model):
    """Game ratings"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='game_ratings')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'game']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.game.name} ({self.rating}/5)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update game average rating
        self.game.average_rating = self.game.ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        self.game.save(update_fields=['average_rating'])


class DailyMemoryImages(models.Model):
    """Daily set of images for Memory Match game"""
    date = models.DateField(unique=True)
    theme = models.CharField(max_length=200, help_text="Daily theme (e.g., 'Lingerie & Lace', 'Red Hot Passion')")
    description = models.TextField(blank=True)
    images = models.JSONField(
        help_text="Array of 8 image URLs for the memory game",
        default=list
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Daily Memory Images"
        ordering = ['-date']

    def __str__(self):
        return f"Memory Images - {self.date} - {self.theme}"
