from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator

class GroceryItemManager(models.Manager):
    def increment_usage(self, item_id):
        # Use F expressions to ensure atomic updates.
        return self.filter(id=item_id).update(usage_count=F('usage_count') + 1)

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.PositiveIntegerField(default=0)  # Represents the group number.
    done = models.BooleanField(default=False)
    order = models.PositiveIntegerField(null=True, blank=True)  # Persistent rank
    last_done_date = models.DateField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    
    objects = GroceryItemManager()

    class Meta:
        ordering = ['-usage_count', 'name']  # Or change this ordering as needed

    def __str__(self):
        return self.name
