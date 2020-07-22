# Python imports
from slugify import slugify

# Django imports
from django.db import models

class FlowerCategory(models.Model):
    name = models.CharField(max_length=191)
    slug = models.CharField(max_length=191)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        slug_str = slugify(self.name)
        self.slug = slug_str
        super(FlowerCategory, self).save(*args, **kwargs) 

    class Meta:
        db_table = 'flower_category'
