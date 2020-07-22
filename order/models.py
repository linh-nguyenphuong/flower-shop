# Django imports
from django.db import models

# Model imports
from user.models import User

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    checkout = models.BooleanField(default=False)
    customer = models.ForeignKey(User, related_name='user', on_delete=models.Case)

    class Meta:
        db_table = 'order'
