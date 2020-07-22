# Rest framework imports
from rest_framework import serializers

# Model imports
from goods_receipt.models import GoodsReceipt
from order.models import Order

# Serializer imports
from flower.admin.serializers import SummaryFlowerSerializer

class RevenueStatisticSerializer(serializers.Serializer):
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    expenses_total = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=0)
    total_revenue = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=0)
    net_income = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=0)
    class Meta:
        fields = (
            'month',
            'year',
            'expenses_total',
            'total_revenue',
            'net_income',
        )

class FlowerStatisticSerializer(serializers.Serializer):
    flower = SummaryFlowerSerializer(
        many=False,
        read_only=True
    )
    flower__name = serializers.CharField(read_only=True)
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=0)
    class Meta:
        fields = (
            'flower__name',
            'month',
            'year',
            'total_quantity',
            'total_price',
        )