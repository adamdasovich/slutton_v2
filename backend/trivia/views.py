from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db.models import F
from datetime import date, timedelta
from .models import DailyTrivia, TriviaQuestion, TriviaGameSession, TriviaAnswer, UserTriviaStats
from .serializers import (
    DailyTriviaSerializer,
    TriviaGameSessionSerializer,
    TriviaAnswerSerializer,
    UserTriviaStatsSerializer,
    LeaderboardSerializer,
    TriviaQuestionWithAnswerSerializer
)


class TriviaViewSet(viewsets.ViewSet):
    """Trivia game viewset"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def today(self, request):
        """Get today's trivia game"""
        today = date.today()

        try:
            daily_trivia = DailyTrivia.objects.prefetch_related('questions').get(
                date=today,
                is_active=True
            )
        except DailyTrivia.DoesNotExist:
            return Response(
                {'error': 'No trivia game available for today'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user already played today (only for authenticated users)
        has_played = False
        if request.user.is_authenticated:
            has_played = TriviaGameSession.objects.filter(
                user=request.user,
                daily_trivia=daily_trivia,
                status__in=['completed', 'in_progress']
            ).exists()

        serializer = DailyTriviaSerializer(daily_trivia)
        return Response({
            'trivia': serializer.data,
            'has_played': has_played,
            'time_limit_seconds': 300  # 5 minutes
        })

    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new game session"""
        today = date.today()

        try:
            daily_trivia = DailyTrivia.objects.get(date=today, is_active=True)
        except DailyTrivia.DoesNotExist:
            return Response(
                {'error': 'No trivia game available for today'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user already has a session today
        existing_session = TriviaGameSession.objects.filter(
            user=request.user,
            daily_trivia=daily_trivia
        ).first()

        if existing_session:
            if existing_session.status == 'completed':
                return Response(
                    {'error': 'You have already completed today\'s trivia'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Return existing in_progress session
                serializer = TriviaGameSessionSerializer(existing_session)
                return Response(serializer.data)

        # Create new session
        session = TriviaGameSession.objects.create(
            user=request.user,
            daily_trivia=daily_trivia
        )

        # Get or create user stats
        UserTriviaStats.objects.get_or_create(user=request.user)

        serializer = TriviaGameSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def submit_answer(self, request):
        """Submit an answer to a question"""
        session_id = request.data.get('session_id')
        question_id = request.data.get('question_id')
        user_answer = request.data.get('answer')
        time_taken = request.data.get('time_taken_seconds', 0)

        try:
            session = TriviaGameSession.objects.get(
                id=session_id,
                user=request.user,
                status='in_progress'
            )
            question = TriviaQuestion.objects.get(id=question_id)
        except (TriviaGameSession.DoesNotExist, TriviaQuestion.DoesNotExist):
            return Response(
                {'error': 'Invalid session or question'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already answered
        if TriviaAnswer.objects.filter(session=session, question=question).exists():
            return Response(
                {'error': 'Question already answered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check answer
        is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
        points_earned = question.max_points if is_correct else 0

        # Create answer record
        answer = TriviaAnswer.objects.create(
            session=session,
            question=question,
            user_answer=user_answer,
            is_correct=is_correct,
            points_earned=points_earned,
            time_taken_seconds=time_taken
        )

        # Update session score
        session.score += points_earned
        session.save()

        return Response({
            'is_correct': is_correct,
            'points_earned': points_earned,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'current_score': session.score
        })

    @action(detail=False, methods=['post'])
    def complete(self, request):
        """Complete the game session"""
        session_id = request.data.get('session_id')
        total_time = request.data.get('total_time_seconds', 0)

        try:
            session = TriviaGameSession.objects.get(
                id=session_id,
                user=request.user,
                status='in_progress'
            )
        except TriviaGameSession.DoesNotExist:
            return Response(
                {'error': 'Invalid session'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark session as completed
        session.status = 'completed'
        session.time_taken_seconds = total_time
        session.completed_at = timezone.now()
        session.save()

        # Update user stats
        stats, created = UserTriviaStats.objects.get_or_create(user=request.user)
        stats.total_games_played += 1
        stats.last_played_date = date.today()

        # Update streak
        if stats.last_played_date:
            days_diff = (date.today() - stats.last_played_date).days
            if days_diff == 1:
                stats.current_streak += 1
            elif days_diff > 1:
                stats.current_streak = 1
        else:
            stats.current_streak = 1

        if stats.current_streak > stats.longest_streak:
            stats.longest_streak = stats.current_streak

        # Check for perfect game
        total_questions = session.daily_trivia.questions.count()
        correct_answers = session.answers.filter(is_correct=True).count()
        if correct_answers == total_questions and total_questions > 0:
            stats.perfect_games += 1

        stats.save()

        # Calculate rank and award placement points
        rank = self._calculate_rank(session)
        placement_points = self._get_placement_points(rank)
        participation_points = 10

        total_bonus_points = placement_points + participation_points
        stats.add_points(total_bonus_points)

        # Update placement stats
        if rank == 1:
            stats.first_place_finishes += 1
        elif rank == 2:
            stats.second_place_finishes += 1
        elif rank == 3:
            stats.third_place_finishes += 1
        stats.save()

        return Response({
            'final_score': session.final_score,
            'rank': rank,
            'placement_points': placement_points,
            'participation_points': participation_points,
            'total_bonus_points': total_bonus_points,
            'perfect_game': correct_answers == total_questions
        })

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get today's leaderboard"""
        today = date.today()

        try:
            daily_trivia = DailyTrivia.objects.get(date=today)
        except DailyTrivia.DoesNotExist:
            return Response([])

        # Get completed sessions, ordered by final_score (desc) then time (asc)
        sessions = TriviaGameSession.objects.filter(
            daily_trivia=daily_trivia,
            status='completed'
        ).select_related('user').order_by('-score', 'time_taken_seconds')[:50]

        # Add rank
        leaderboard_data = []
        for rank, session in enumerate(sessions, 1):
            leaderboard_data.append({
                'rank': rank,
                'username': session.user.username,
                'final_score': session.final_score,
                'time_taken_seconds': session.time_taken_seconds,
                'completed_at': session.completed_at
            })

        return Response(leaderboard_data)

    @action(detail=False, methods=['get'])
    def my_stats(self, request):
        """Get user's trivia stats"""
        stats, created = UserTriviaStats.objects.get_or_create(user=request.user)
        serializer = UserTriviaStatsSerializer(stats)
        return Response(serializer.data)

    def _calculate_rank(self, session):
        """Calculate user's rank for the day"""
        better_sessions = TriviaGameSession.objects.filter(
            daily_trivia=session.daily_trivia,
            status='completed'
        ).filter(
            score__gt=session.score
        ).count()

        # For ties, check time
        tie_sessions = TriviaGameSession.objects.filter(
            daily_trivia=session.daily_trivia,
            status='completed',
            score=session.score,
            time_taken_seconds__lt=session.time_taken_seconds
        ).count()

        return better_sessions + tie_sessions + 1

    def _get_placement_points(self, rank):
        """Get bonus points for placement"""
        placement_rewards = {
            1: 100,  # 1st place
            2: 50,   # 2nd place
            3: 25,   # 3rd place
        }
        return placement_rewards.get(rank, 0)
