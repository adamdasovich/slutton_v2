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
try:
    call_command('loaddata', 'datadump.json', verbosity=2)
    print("\n✅ Successfully imported all data!")
except Exception as e:
    print(f"\n❌ Error during import: {e}")
    sys.exit(1)
