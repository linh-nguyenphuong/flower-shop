# Django imports
from django.db import models

# Model imports
from order.models import Order

class Shipping(models.Model):
    ship_date = models.DateField()
    address = models.CharField(max_length=191)
    is_shipped = models.BooleanField(default=False)
    order = models.ForeignKey(Order, related_name='shipping_order', on_delete=models.Case)

    class Meta:
        db_table = 'shipping'
