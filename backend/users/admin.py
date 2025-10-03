from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'age_verified', 'date_of_birth', 'is_staff']
    list_filter = ['age_verified', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age_verified', 'date_of_birth', 'phone_number')}),
    )
