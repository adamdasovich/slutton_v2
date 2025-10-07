from rest_framework import serializers
from .models import DailyTrivia, TriviaQuestion, TriviaGameSession, TriviaAnswer, UserTriviaStats


class TriviaQuestionSerializer(serializers.ModelSerializer):
    """Trivia question serializer (hides correct answer until answered)"""
    class Meta:
        model = TriviaQuestion
        fields = [
            'id', 'question_text', 'question_type', 'difficulty',
            'option_a', 'option_b', 'option_c', 'option_d', 'options',
            'order', 'max_points'
        ]


class TriviaQuestionWithAnswerSerializer(serializers.ModelSerializer):
    """Trivia question with answer (for results)"""
    class Meta:
        model = TriviaQuestion
        fields = [
            'id', 'question_text', 'question_type', 'difficulty',
            'option_a', 'option_b', 'option_c', 'option_d', 'options',
            'correct_answer', 'explanation', 'order', 'max_points'
        ]


class DailyTriviaSerializer(serializers.ModelSerializer):
    """Daily trivia serializer"""
    questions = TriviaQuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = DailyTrivia
        fields = ['id', 'date', 'theme', 'description', 'questions', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()


class TriviaAnswerSerializer(serializers.ModelSerializer):
    """Trivia answer serializer"""
    question_text = serializers.CharField(source='question.question_text', read_only=True)

    class Meta:
        model = TriviaAnswer
        fields = [
            'id', 'question', 'question_text', 'user_answer',
            'is_correct', 'points_earned', 'time_taken_seconds', 'answered_at'
        ]
        read_only_fields = ['is_correct', 'points_earned', 'answered_at']


class TriviaGameSessionSerializer(serializers.ModelSerializer):
    """Game session serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    daily_trivia_theme = serializers.CharField(source='daily_trivia.theme', read_only=True)
    answers = TriviaAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = TriviaGameSession
        fields = [
            'id', 'user', 'username', 'daily_trivia', 'daily_trivia_theme',
            'status', 'score', 'final_score', 'time_taken_seconds',
            'started_at', 'completed_at', 'answers'
        ]
        read_only_fields = ['user', 'score', 'started_at', 'completed_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Leaderboard entry serializer"""
    username = serializers.CharField(source='user.username')
    rank = serializers.IntegerField()

    class Meta:
        model = TriviaGameSession
        fields = ['rank', 'username', 'final_score', 'time_taken_seconds', 'completed_at']


class UserTriviaStatsSerializer(serializers.ModelSerializer):
    """User trivia stats serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = UserTriviaStats
        fields = [
            'username', 'total_games_played', 'total_points_earned',
            'available_points', 'discount_amount',
            'first_place_finishes', 'second_place_finishes', 'third_place_finishes',
            'current_streak', 'longest_streak', 'last_played_date', 'perfect_games'
        ]

    def get_discount_amount(self, obj):
        """Calculate discount amount (1 point = $0.10)"""
        return round(obj.available_points * 0.10, 2)
