"""
Delete all existing trivia and regenerate with new question pool
Run this: python regenerate_all_trivia.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from trivia.models import DailyTrivia
from django.core.management import call_command

def regenerate_trivia():
    # Delete ALL existing trivia
    count = DailyTrivia.objects.all().count()
    DailyTrivia.objects.all().delete()
    print(f"✅ Deleted {count} existing trivia entries")

    # Regenerate for next 7 days
    print("\nGenerating fresh trivia for next 7 days...")
    call_command('generate_trivia_week', '--days', '7')

    print("\n✅ Done! All trivia has been regenerated with new questions")

if __name__ == "__main__":
    regenerate_trivia()
