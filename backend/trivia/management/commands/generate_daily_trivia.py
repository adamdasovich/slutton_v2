"""
Management command to generate daily trivia using Claude AI
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from trivia.models import DailyTrivia, TriviaQuestion
from trivia.claude_service import ClaudeTriviaGenerator


class Command(BaseCommand):
    help = 'Generate daily trivia questions using Claude AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for trivia (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--days-ahead',
            type=int,
            default=0,
            help='Generate trivia for X days ahead (default: 0 = today only)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate even if trivia exists for the date',
        )

    def handle(self, *args, **options):
        generator = ClaudeTriviaGenerator()

        # Determine date(s) to generate
        if options['date']:
            try:
                start_date = date.fromisoformat(options['date'])
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                )
                return
        else:
            start_date = date.today()

        days_ahead = options['days_ahead']
        force = options['force']

        # Generate for each day
        for day_offset in range(days_ahead + 1):
            trivia_date = start_date + timedelta(days=day_offset)

            # Check if already exists
            if DailyTrivia.objects.filter(date=trivia_date).exists():
                if not force:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Trivia already exists for {trivia_date}. Use --force to regenerate.'
                        )
                    )
                    continue
                else:
                    # Delete existing
                    DailyTrivia.objects.filter(date=trivia_date).delete()
                    self.stdout.write(
                        self.style.WARNING(f'Deleted existing trivia for {trivia_date}')
                    )

            self.stdout.write(f'Generating trivia for {trivia_date}...')

            try:
                # Generate questions using Claude
                trivia_data = generator.generate_daily_trivia(trivia_date)

                # Create DailyTrivia
                daily_trivia = DailyTrivia.objects.create(
                    date=trivia_date,
                    theme=trivia_data['theme'],
                    description=trivia_data['description'],
                    is_active=True
                )

                # Create questions
                questions_created = 0
                for q_data in trivia_data['questions']:
                    # Validate question structure
                    generator.validate_question_structure(q_data)

                    # Serialize options for storage
                    options_json = None
                    if q_data['question_type'] == 'multiple_choice':
                        options_json = q_data['options']

                    TriviaQuestion.objects.create(
                        daily_trivia=daily_trivia,
                        order=q_data['order'],
                        question_text=q_data['question_text'],
                        question_type=q_data['question_type'],
                        difficulty=q_data['difficulty'],
                        options=options_json,
                        correct_answer=q_data['correct_answer'],
                        explanation=q_data['explanation']
                        # max_points is calculated from difficulty via @property
                    )
                    questions_created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created trivia for {trivia_date}: {trivia_data["theme"]} ({questions_created} questions)'
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error generating trivia for {trivia_date}: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'\nDone! Generated trivia for {days_ahead + 1} day(s)')
        )
