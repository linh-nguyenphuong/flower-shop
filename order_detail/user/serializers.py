# Rest framework imports
from rest_framework import serializers

# Model imports
from order_detail.models import (
    OrderDetail
)

# Serializer imports
from flower.user.serializers import FlowerSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    flower = FlowerSerializer(
        many=False,
        read_only=True
    )
    flower_id = serializers.CharField(write_only=True)

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'quantity',
            'unit_price',
            'flower_id',
            'flower',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'unit_price': {'read_only': True}
        }

