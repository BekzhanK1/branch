from django.db import models
from django.utils.timezone import now
from company.models import Company, Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class WarehouseProduct(models.Model):
    
    class Status(models.Choices):
        SOLD = "sold"
        AVAILABLE = "available"
        
    name = models.CharField(max_length = 255)
    date_added = models.DateTimeField(default = now)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    total_price = models.FloatField(blank = True)
    status = models.CharField(max_length = 40, choices = Status.choices, default = Status.AVAILABLE)
    
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    receiver_staff = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(default = now)