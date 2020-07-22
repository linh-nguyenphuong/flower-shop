# Django imports
from django.db import models

# Model imports
from flower.models import Flower
from supplier.models import Supplier

class GoodsReceipt(models.Model):
    historical_cost = models.DecimalField(max_digits=20, decimal_places=0)
    receipt_quantity = models.IntegerField()
    residual_quantity = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True) # False: Sold out or Expired
    flower = models.ForeignKey(Flower, related_name='goods_receipt_flower', on_delete=models.Case)
    supplier = models.ForeignKey(Supplier, related_name='goods_receipt_supplier', on_delete=models.Case)

    class Meta:
        db_table = 'goods_receipt'

