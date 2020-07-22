# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from shipping.models import Shipping

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = (
            'id',
            'ship_date',
            'address',
            'is_shipped',
            'order_id'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'order_id': {'read_only': True},
            'ship_date': {'required': False},
            'address': {'required': False},
            'is_shipped': {'required': False},
        }

