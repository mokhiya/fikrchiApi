from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise ValidationError("Email must be only a gmail address")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
