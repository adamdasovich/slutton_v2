from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age_verified', 'date_of_birth', 'phone_number', 'created_at', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'created_at', 'is_staff', 'is_superuser']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'date_of_birth']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user


class AgeVerificationSerializer(serializers.Serializer):
    """Age verification serializer"""
    date_of_birth = serializers.DateField(required=True)
    confirm_over_18 = serializers.BooleanField(required=True)

    def validate(self, attrs):
        from datetime import date, timedelta
        dob = attrs['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 18:
            raise serializers.ValidationError("You must be 18 or older to access this site.")

        if not attrs['confirm_over_18']:
            raise serializers.ValidationError("You must confirm you are over 18 years old.")

        return attrs
