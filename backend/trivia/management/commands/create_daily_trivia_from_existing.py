"""
Management command to create daily trivia from existing questions
"""
from django.core.management.base import BaseCommand
from datetime import date
from trivia.models import DailyTrivia, TriviaQuestion
import random


class Command(BaseCommand):
    help = 'Create daily trivia from existing questions in database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate even if trivia exists for today',
        )

    def handle(self, *args, **options):
        today = date.today()
        force = options['force']

        # Check if already exists
        if DailyTrivia.objects.filter(date=today).exists():
            if not force:
                self.stdout.write(
                    self.style.WARNING(
                        f'Trivia already exists for {today}. Use --force to regenerate.'
                    )
                )
                return
            else:
                # Delete existing
                DailyTrivia.objects.filter(date=today).delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted existing trivia for {today}')
                )

        # Get all existing trivia questions
        all_questions = list(TriviaQuestion.objects.all())

        if len(all_questions) < 15:
            self.stdout.write(
                self.style.ERROR(
                    f'Not enough questions in database. Found {len(all_questions)}, need at least 15'
                )
            )
            return

        self.stdout.write(f'Found {len(all_questions)} total questions in database')

        # Randomly select 15 questions
        selected_questions = random.sample(all_questions, min(15, len(all_questions)))

        # Create DailyTrivia
        daily_trivia = DailyTrivia.objects.create(
            date=today,
            theme="Daily Challenge",
            description="Test your knowledge with today's curated trivia questions",
            is_active=True
        )

        # Create copies of selected questions for today's trivia
        for index, original_question in enumerate(selected_questions, 1):
            TriviaQuestion.objects.create(
                daily_trivia=daily_trivia,
                order=index,
                question_text=original_question.question_text,
                question_type=original_question.question_type,
                difficulty=original_question.difficulty,
                options=original_question.options,
                correct_answer=original_question.correct_answer,
                explanation=original_question.explanation
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Created daily trivia for {today} with {len(selected_questions)} questions'
            )
        )
