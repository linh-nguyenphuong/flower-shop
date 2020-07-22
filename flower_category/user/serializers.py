# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from flower_category.models import FlowerCategory

class FlowerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerCategory
        fields = (
            'id',
            'name',
            'slug'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'slug': {'read_only': True}
        }

