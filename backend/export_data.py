"""
Export database data with proper UTF-8 encoding
Run with: python export_data.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from django.core import serializers
from django.apps import apps

def export_data():
    """Export all data with UTF-8 encoding"""

    # Get all models except the ones we want to exclude
    all_objects = []

    for model in apps.get_models():
        # Skip contenttypes and permissions
        if model._meta.app_label == 'contenttypes':
            continue
        if model._meta.model_name == 'permission' and model._meta.app_label == 'auth':
            continue

        # Get all objects from this model
        objects = model.objects.all()
        all_objects.extend(objects)

    # Serialize with UTF-8
    print(f"Exporting {len(all_objects)} objects...")

    data = serializers.serialize(
        'json',
        all_objects,
        indent=2,
        use_natural_foreign_keys=True,
        use_natural_primary_keys=True
    )

    # Write with explicit UTF-8 encoding
    with open('datadump.json', 'w', encoding='utf-8') as f:
        f.write(data)

    print(f"Successfully exported to datadump.json")
    print(f"File size: {len(data) / 1024:.2f} KB")

if __name__ == '__main__':
    try:
        export_data()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
