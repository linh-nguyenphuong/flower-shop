# Django imports

# Rest framework imports
from rest_framework import serializers

# Base import

# Application imports

# Model imports
from user.models import (
    User
)

# Serializer imports

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'DOB',
            'address',
            'avatar',
            'created_at',
            'is_staff',
            'is_active'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
            'avatar': {'read_only': True},
            'created_at': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        }

class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'is_staff',
            'is_active'
        )
