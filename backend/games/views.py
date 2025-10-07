from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import date
from .models import GameCategory, Game, GameProgress, GameRating, DailyMemoryImages
from .serializers import (
    GameCategorySerializer,
    GameSerializer,
    GameProgressSerializer,
    GameRatingSerializer
)


class GameCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Game category viewset"""
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    lookup_field = 'slug'


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """Game viewset"""
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_featured']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['play_count', 'average_rating', 'created_at']
    ordering = ['-is_featured', '-play_count']

    @action(detail=True, methods=['post'])
    def play(self, request, slug=None):
        """Increment play count"""
        game = self.get_object()
        game.increment_play_count()

        # Create or update user progress if authenticated
        if request.user.is_authenticated:
            progress, created = GameProgress.objects.get_or_create(
                user=request.user,
                game=game
            )
            progress.save()  # Updates last_played

        return Response({'play_count': game.play_count})

    @action(detail=True, methods=['get'])
    def ratings(self, request, slug=None):
        """Get game ratings"""
        game = self.get_object()
        ratings = game.ratings.all()[:10]
        serializer = GameRatingSerializer(ratings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, slug=None):
        """Rate a game"""
        game = self.get_object()
        serializer = GameRatingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Update or create rating
            rating, created = GameRating.objects.update_or_create(
                user=request.user,
                game=game,
                defaults={
                    'rating': serializer.validated_data['rating'],
                    'review': serializer.validated_data.get('review', '')
                }
            )
            return Response(
                GameRatingSerializer(rating).data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request, slug=None):
        """Mark game as completed and save score"""
        game = self.get_object()
        score = request.data.get('score', 0)
        time_taken = request.data.get('time_taken', 0)
        moves = request.data.get('moves', 0)

        # Update or create progress
        progress, created = GameProgress.objects.update_or_create(
            user=request.user,
            game=game,
            defaults={
                'completed': True,
                'progress_data': {
                    'score': score,
                    'time_taken_seconds': time_taken,
                    'moves': moves,
                    'completed_at': str(request.data.get('completed_at', ''))
                },
                'play_time_minutes': time_taken // 60
            }
        )

        return Response({
            'message': 'Game completed successfully',
            'score': score,
            'progress_id': progress.id
        }, status=status.HTTP_200_OK)


class GameProgressViewSet(viewsets.ModelViewSet):
    """Game progress viewset"""
    serializer_class = GameProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GameProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MemoryImagesViewSet(viewsets.ViewSet):
    """Memory game images viewset"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's memory game images"""
        today = date.today()

        try:
            daily_images = DailyMemoryImages.objects.get(
                date=today,
                is_active=True
            )
        except DailyMemoryImages.DoesNotExist:
            return Response(
                {'error': 'No images available for today. Contact admin to generate.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'date': daily_images.date,
            'theme': daily_images.theme,
            'description': daily_images.description,
            'images': daily_images.images
        })
