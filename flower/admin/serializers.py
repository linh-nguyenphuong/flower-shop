# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from flower.models import (
    Flower,
    FlowerImage
)

# Serializer imports
from flower_category.admin.serializers import FlowerCategorySerializer

class FlowerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerImage
        fields = (
            'id',
            'url',
            'is_main'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'url': {'read_only': True},
            'is_main': {'read_only': True},
        }

class FlowerSerializer(serializers.ModelSerializer):
    flower_category = FlowerCategorySerializer(
        many=False,
        read_only=True
    )
    flower_category_id = serializers.CharField(write_only=True)

    images = serializers.SerializerMethodField('get_images')
    def get_images(self, flower):
        queryset = FlowerImage.objects.filter(
            flower=flower
        )
        serializer = FlowerImageSerializer(instance=queryset, many=True)
        return serializer.data

    class Meta:
        model = Flower
        fields = (
            'id',
            'name',
            'price',
            'detail',
            'images',
            'flower_category_id',
            'flower_category',
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }

class SummaryFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = (
            'id',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }