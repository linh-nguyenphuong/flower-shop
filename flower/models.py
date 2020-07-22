# Python imports
from slugify import slugify
import uuid
import os

# Django imports
from django.db import models
from django.utils.crypto import get_random_string

# Model imports
from flower_category.models import FlowerCategory

class Flower(models.Model):
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    detail = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=191)
    is_deleted = models.BooleanField(default=False)
    flower_category = models.ForeignKey(FlowerCategory, related_name='flower_category', on_delete=models.Case)

    def save(self, *args, **kwargs): 
        slug_str = slugify(self.name)
        self.slug = slug_str
        super(Flower, self).save(*args, **kwargs) 

    class Meta:
        db_table = 'flower'

class FlowerImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flower = models.ForeignKey(Flower, related_name='flower', on_delete=models.Case, null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def _get_file_path(instance, filename):
        unique_id = get_random_string(length=100)
        name, extension = os.path.splitext(filename) 
        filename = unique_id + extension
        return '{0}/{1}'.format('flower_images', filename)

    url = models.ImageField(upload_to=_get_file_path)

    class Meta:
        db_table = 'flower_image'

