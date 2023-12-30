from django.db import models
from django.utils.timezone import now


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.DurationField()
    popularity = models.IntegerField(default=0)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.name + ' ' + self.price
