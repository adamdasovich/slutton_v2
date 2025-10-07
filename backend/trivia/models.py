from django.db import models
from django.utils import timezone
from users.models import CustomUser
import random


class DailyTrivia(models.Model):
    """Daily trivia game configuration"""
    date = models.DateField(unique=True, default=timezone.now)
    theme = models.CharField(max_length=100, help_text="e.g., 'Seductive History', 'Pleasure Science'")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Daily Trivia Games"
        ordering = ['-date']

    def __str__(self):
        return f"Trivia - {self.date} - {self.theme}"


class TriviaQuestion(models.Model):
    """Individual trivia questions"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    daily_trivia = models.ForeignKey(DailyTrivia, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(help_text="The witty, sensual question")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')

    # For multiple choice questions (legacy format)
    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)

    # New format for Claude-generated questions (JSON)
    options = models.JSONField(null=True, blank=True, help_text="Options as JSON: {'A': 'text', 'B': 'text', ...}")

    correct_answer = models.CharField(max_length=200, help_text="The correct answer")
    explanation = models.TextField(blank=True, help_text="Witty explanation after answering")

    # Points based on difficulty
    points_easy = models.IntegerField(default=10)
    points_medium = models.IntegerField(default=20)
    points_hard = models.IntegerField(default=30)

    order = models.IntegerField(default=0, help_text="Question order in the game")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['daily_trivia', 'order']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"

    @property
    def max_points(self):
        """Get max points for this question based on difficulty"""
        points_map = {
            'easy': self.points_easy,
            'medium': self.points_medium,
            'hard': self.points_hard,
        }
        return points_map.get(self.difficulty, 20)


class TriviaGameSession(models.Model):
    """User's game session for a specific day"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trivia_sessions')
    daily_trivia = models.ForeignKey(DailyTrivia, on_delete=models.CASCADE, related_name='sessions')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0, help_text="Total time taken in seconds")

    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'daily_trivia']
        ordering = ['-score', 'time_taken_seconds']

    def __str__(self):
        return f"{self.user.username} - {self.daily_trivia.date} - Score: {self.score}"

    def calculate_final_score(self):
        """Calculate final score with time bonus"""
        # Base score from correct answers
        base_score = self.score

        # Time bonus: faster players get more points (max 50 bonus points)
        # 5 minutes = 300 seconds, bonus = 50 - (time_taken / 6)
        time_bonus = max(0, 50 - (self.time_taken_seconds // 6))

        return base_score + time_bonus

    @property
    def final_score(self):
        return self.calculate_final_score()


class TriviaAnswer(models.Model):
    """User's answer to a specific question"""
    session = models.ForeignKey(TriviaGameSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE, related_name='user_answers')

    user_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0, help_text="Time taken to answer this question")

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['answered_at']

    def __str__(self):
        return f"{self.session.user.username} - Q{self.question.order} - {'✓' if self.is_correct else '✗'}"


class UserTriviaStats(models.Model):
    """Overall trivia statistics for a user"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='trivia_stats')

    # Lifetime stats
    total_games_played = models.IntegerField(default=0)
    total_points_earned = models.IntegerField(default=0)
    first_place_finishes = models.IntegerField(default=0)
    second_place_finishes = models.IntegerField(default=0)
    third_place_finishes = models.IntegerField(default=0)

    # Current redeemable points
    available_points = models.IntegerField(default=0, help_text="Points available for discounts")

    # Streak
    current_streak = models.IntegerField(default=0, help_text="Consecutive days played")
    longest_streak = models.IntegerField(default=0)
    last_played_date = models.DateField(null=True, blank=True)

    # Achievements
    perfect_games = models.IntegerField(default=0, help_text="Games with 100% correct answers")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Trivia Stats"

    def __str__(self):
        return f"{self.user.username} - {self.available_points} pts"

    def add_points(self, points):
        """Add points to user's available balance"""
        self.available_points += points
        self.total_points_earned += points
        self.save()

    def redeem_points(self, points):
        """Redeem points for discount"""
        if self.available_points >= points:
            self.available_points -= points
            self.save()
            return True
        return False
