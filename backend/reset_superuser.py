"""
Reset superuser password from environment variables
Run on Railway by setting RUN_PASSWORD_RESET=true
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings_production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'adamd')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

if not password:
    print("ERROR: DJANGO_SUPERUSER_PASSWORD not set!")
    sys.exit(1)

try:
    # Try to get existing user
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"✅ Password updated for user: {username}")
except User.DoesNotExist:
    # Create new superuser
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Created new superuser: {username}")
