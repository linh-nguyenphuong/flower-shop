# Django imports
from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=191)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=191, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'supplier'

