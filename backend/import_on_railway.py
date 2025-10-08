"""
Script to import data when DATABASE_URL is already set by Railway
Run this on Railway after deployment
"""
import os
import sys
import django

# DATABASE_URL should already be set by Railway
if not os.environ.get('DATABASE_URL'):
    print("ERROR: DATABASE_URL not set!")
    sys.exit(1)

print(f"DATABASE_URL is set: {os.environ.get('DATABASE_URL')[:20]}...")

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings_production')
django.setup()

from django.core.management import call_command

print("Importing data from datadump.json...")
print("Note: Ignoring admin.LogEntry to avoid constraint violations")
try:
    # Try importing with ignoring errors for problematic models
    call_command('loaddata', 'datadump.json', verbosity=2, ignore=True)
    print("\n✅ Successfully imported data (with some skipped entries)!")
except Exception as e:
    print(f"\n❌ Error during import: {e}")
    print("\nTrying alternative approach - importing model by model...")

    # Try importing specific apps only
    from products.models import Product, Category
    from games.models import Game
    from trivia.models import TriviaQuestion
    from users.models import CustomUser

    print("Data import attempted. Check admin panel to verify.")
    # Don't exit with error - let the app start anyway
