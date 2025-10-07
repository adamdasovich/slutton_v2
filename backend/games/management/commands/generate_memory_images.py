"""
Management command to generate daily memory game images using Claude AI
"""
from django.core.management.base import BaseCommand
from datetime import date, timedelta
from games.models import DailyMemoryImages
from games.claude_image_service import ClaudeImageGenerator


class Command(BaseCommand):
    help = 'Generate daily memory game images using Claude AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for images (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--days-ahead',
            type=int,
            default=0,
            help='Generate images for X days ahead (default: 0 = today only)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate even if images exist for the date',
        )

    def handle(self, *args, **options):
        generator = ClaudeImageGenerator()

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
        success_count = 0
        for day_offset in range(days_ahead + 1):
            image_date = start_date + timedelta(days=day_offset)

            # Check if already exists
            if DailyMemoryImages.objects.filter(date=image_date).exists():
                if not force:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Images already exist for {image_date}. Use --force to regenerate.'
                        )
                    )
                    continue
                else:
                    # Delete existing
                    DailyMemoryImages.objects.filter(date=image_date).delete()
                    self.stdout.write(
                        self.style.WARNING(f'Deleted existing images for {image_date}')
                    )

            self.stdout.write(f'Generating images for {image_date}...')

            try:
                # Generate images using Claude
                image_data = generator.generate_daily_images(image_date)

                # Create DailyMemoryImages
                daily_images = DailyMemoryImages.objects.create(
                    date=image_date,
                    theme=image_data['theme'],
                    description=image_data['description'],
                    images=image_data['images'],
                    is_active=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created images for {image_date}: {image_data["theme"]} ({len(image_data["images"])} images)'
                    )
                )
                success_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error generating images for {image_date}: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'\nDone! Generated images for {success_count} day(s)')
        )
