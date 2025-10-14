"""
Management command to generate trivia for the next 7 days
Run: python manage.py generate_trivia_week
"""
from django.core.management.base import BaseCommand
from datetime import date, timedelta
from trivia.models import DailyTrivia, TriviaQuestion
import random


class Command(BaseCommand):
    help = 'Generate trivia for the next 7 days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days ahead to generate (default: 7)',
        )

    def handle(self, *args, **options):
        days_ahead = options['days']

        # Pool of themes
        themes = [
            "Sensual Knowledge",
            "Lingerie Legends",
            "Fashion & Desire",
            "Intimate History",
            "Seductive Science",
            "Luxury & Lace",
            "Passion & Style"
        ]

        # Base question templates (15 questions)
        question_templates = self.get_question_templates()

        created_count = 0
        for day_offset in range(days_ahead):
            trivia_date = date.today() + timedelta(days=day_offset)

            # Check if already exists
            if DailyTrivia.objects.filter(date=trivia_date).exists():
                self.stdout.write(f"Trivia already exists for {trivia_date}")
                continue

            # Create DailyTrivia with random theme
            theme = random.choice(themes)
            daily_trivia = DailyTrivia.objects.create(
                date=trivia_date,
                theme=theme,
                description=f"Test your knowledge with today's {theme.lower()} trivia questions",
                is_active=True
            )

            # Randomly select 15 questions from the pool
            questions = random.sample(question_templates, 15)

            # Create questions
            for order, q_data in enumerate(questions, 1):
                TriviaQuestion.objects.create(
                    daily_trivia=daily_trivia,
                    order=order,
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    difficulty=q_data["difficulty"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"]
                )

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created trivia for {trivia_date}: {theme}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nDone! Generated trivia for {created_count} day(s)")
        )

    def get_question_templates(self):
        """Return pool of 100+ trivia questions"""
        from trivia.question_pool import QUESTION_POOL
        return QUESTION_POOL
