# Rest framework imports
from rest_framework import serializers

# Model imports
from order.models import (
    Order
)
from order_detail.models import OrderDetail

# Serializer imports
from user.profile.serializers import PublicProfileSerializer
from order_detail.user.serializers import OrderDetailSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = PublicProfileSerializer(
        many=False,
        read_only=True
    )

    order_details = serializers.SerializerMethodField('get_order_details')
    def get_order_details(self, order):
        queryset = OrderDetail.objects.filter(
            order=order
        )
        serializer = OrderDetailSerializer(instance=queryset, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'total',
            'checkout',
            'customer',
            'order_details',
        )

