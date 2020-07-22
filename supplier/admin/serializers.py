# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports

# Model imports
from supplier.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'phone',
            'address'
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }

