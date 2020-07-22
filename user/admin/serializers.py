# Rest framework imports
from rest_framework import serializers


# Model imports
from user.models import (
    User
)

class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'created_at'
        )
