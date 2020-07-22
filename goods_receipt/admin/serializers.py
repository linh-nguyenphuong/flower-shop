# Rest framework imports
from rest_framework import serializers

# Model imports
from goods_receipt.models import GoodsReceipt

# Serializer imports
from flower.admin.serializers import FlowerSerializer
from supplier.admin.serializers import SupplierSerializer

class GoodsReceiptSerializer(serializers.ModelSerializer):
    flower = FlowerSerializer(
        read_only=True,
        many=False
    )
    flower_id = serializers.CharField(write_only=True)

    supplier = SupplierSerializer(
        read_only=True,
        many=False
    )
    supplier_id = serializers.CharField(write_only=True)

    class Meta:
        model = GoodsReceipt
        fields = (
            'id',
            'historical_cost',
            'receipt_quantity',
            'residual_quantity',
            'created_at',
            'expired_date',
            'is_active',
            'flower_id',
            'flower',
            'supplier_id',
            'supplier',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'residual_quantity': {'read_only': True},
            'created_at': {'read_only': True}
        }

