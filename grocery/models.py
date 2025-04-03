from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator

class Group(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class GroceryItemManager(models.Manager):
    def increment_usage(self, item_id):
        # Atomic update using F expressions.
        return self.filter(id=item_id).update(usage_count=F('usage_count') + 1)

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='items')
    done = models.BooleanField(default=False)
    order = models.PositiveIntegerField(null=True, blank=True)  # Persistent rank
    last_done_date = models.DateField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    
    objects = GroceryItemManager()

    class Meta:
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return self.name
