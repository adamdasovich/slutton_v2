"""
Management command to reset and regenerate trivia questions
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from trivia.models import DailyTrivia, TriviaQuestion
from trivia.claude_service import ClaudeTriviaGenerator


class Command(BaseCommand):
    help = 'Reset and regenerate trivia questions for a specific date'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date to reset (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset even if users have already played (deletes their sessions)',
        )
        parser.add_argument(
            '--keep-sessions',
            action='store_true',
            help='Keep user sessions but regenerate questions (WARNING: sessions will be invalid)',
        )

    def handle(self, *args, **options):
        # Determine date
        if options['date']:
            try:
                trivia_date = date.fromisoformat(options['date'])
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                )
                return
        else:
            trivia_date = date.today()

        # Check if trivia exists
        try:
            trivia = DailyTrivia.objects.get(date=trivia_date)
        except DailyTrivia.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'No trivia found for {trivia_date}. Create one first.')
            )
            return

        # Check for existing sessions
        session_count = trivia.sessions.count()

        if session_count > 0 and not options['force'] and not options['keep_sessions']:
            self.stdout.write(
                self.style.WARNING(
                    f'\nWARNING: {session_count} users have already played this trivia!\n'
                    f'   Date: {trivia_date}\n'
                    f'   Theme: {trivia.theme}\n\n'
                    f'Options:\n'
                    f'  --force           Delete all sessions and regenerate (users can replay)\n'
                    f'  --keep-sessions   Keep sessions but regenerate questions (sessions become invalid)\n\n'
                    f'Run again with one of these flags to proceed.'
                )
            )
            return

        # Handle session deletion if forced
        if options['force'] and session_count > 0:
            self.stdout.write(
                self.style.WARNING(f'Deleting {session_count} user sessions...')
            )

            # Delete all answers first
            total_answers = 0
            for session in trivia.sessions.all():
                answer_count = session.answers.count()
                session.answers.all().delete()
                total_answers += answer_count

            # Delete sessions
            trivia.sessions.all().delete()

            self.stdout.write(
                self.style.SUCCESS(f'Deleted {session_count} sessions and {total_answers} answers')
            )

        # Keep sessions warning
        if options['keep_sessions'] and session_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'WARNING: Keeping {session_count} sessions but regenerating questions!\n'
                    f'   This will make existing sessions invalid (wrong question IDs).'
                )
            )

        # Delete existing questions
        question_count = trivia.questions.count()
        trivia.questions.all().delete()
        self.stdout.write(f'Deleted {question_count} existing questions')

        # Generate new questions with Claude
        self.stdout.write(f'Generating new questions with Claude AI...')

        try:
            generator = ClaudeTriviaGenerator()
            trivia_data = generator.generate_daily_trivia(trivia_date)

            # Update theme and description
            trivia.theme = trivia_data['theme']
            trivia.description = trivia_data['description']
            trivia.save()

            # Create questions
            questions_created = 0
            for q_data in trivia_data['questions']:
                generator.validate_question_structure(q_data)

                options_json = None
                if q_data['question_type'] == 'multiple_choice':
                    options_json = q_data['options']

                TriviaQuestion.objects.create(
                    daily_trivia=trivia,
                    order=q_data['order'],
                    question_text=q_data['question_text'],
                    question_type=q_data['question_type'],
                    difficulty=q_data['difficulty'],
                    options=options_json,
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data['explanation']
                )
                questions_created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully regenerated trivia for {trivia_date}\n'
                    f'   Theme: {trivia.theme}\n'
                    f'   Questions: {questions_created}\n'
                    f'   Description: {trivia.description[:100]}...\n'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'\nError generating trivia: {str(e)}\n'
                    f'   Questions were deleted but not replaced!\n'
                    f'   You may need to manually create questions or fix the API key.'
                )
            )
