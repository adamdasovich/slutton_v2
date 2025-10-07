"""
Import database data from datadump.json with proper UTF-8 encoding
Run with: python import_data.py

IMPORTANT: Run migrations first!
    python manage.py migrate
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from django.core.management import call_command

def import_data():
    """Import data from datadump.json"""

    if not os.path.exists('datadump.json'):
        print("Error: datadump.json not found!")
        print("Make sure you're in the backend directory and have run export_data.py first.")
        sys.exit(1)

    print("Importing data from datadump.json...")
    print("This may take a minute...")

    try:
        # Load the data
        call_command('loaddata', 'datadump.json', verbosity=2)
        print("\nSuccessfully imported all data!")
        print("\nNext steps:")
        print("1. Create a superuser: python manage.py createsuperuser")
        print("2. Test your application")

    except Exception as e:
        print(f"\nError during import: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure migrations are up to date: python manage.py migrate")
        print("2. Check that your database is empty or you want to add to existing data")
        print("3. If you get duplicate key errors, you may need to clear the database first")
        sys.exit(1)

if __name__ == '__main__':
    import_data()
