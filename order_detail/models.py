# Django imports
from django.db import models

# Model imports
from order.models import Order
from flower.models import Flower

class OrderDetail(models.Model):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=0)
    order = models.ForeignKey(Order, related_name='order_detail_order', on_delete=models.Case)
    flower = models.ForeignKey(Flower, related_name='order_detail_flower', on_delete=models.Case)

    class Meta:
        db_table = 'order_detail'
