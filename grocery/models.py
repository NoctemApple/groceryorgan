from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator

class GroceryItemManager(models.Manager):
    def increment_usage(self, item_id):
        item = self.get(id=item_id)
        item.usage_count = models.F('usage_count') + 1
        item.save()

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    usage_count = models.PositiveIntegerField(default=0)

    objects = GroceryItemManager()
class GroceryItemManager(models.Manager):
    def increment_usage(self, item_id):
        self.filter(id=item_id).update(usage_count=F('usage_count') + 1)

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    usage_count = models.PositiveIntegerField(default=0)

    objects = GroceryItemManager()

    def __str__(self):
        return self.name

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    usage_count = models.PositiveIntegerField(default=0)

    objects = GroceryItemManager()

    class Meta:
        ordering = ['-usage_count', 'name']

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    usage_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    objects = GroceryItemManager()
