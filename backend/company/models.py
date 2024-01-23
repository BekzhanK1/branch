from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

# Create your models here.

class Company(models.Model):
    
    class CompanyType(models.TextChoices):
        CANTEEN = "canteen"
        CAFE = "cafe"
        COFFEE_SHOP = "coffee_shop"
    
    name = models.CharField(max_length = 255)
    description = models.TextField()
    address = models.CharField(max_length = 255)
    phone_number = models.CharField(max_length = 255)
    type = models.CharField(max_length = 50, choices = CompanyType.choices)

    company_owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "company", default = 63)

    def __str__(self):
        return self.name
    
class CompanyEmployee(models.Model):
    # company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # employee = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField(default = now)

    # def __str__(self):
        # return f"{self.employee} - {self.title} at {self.company}"
    
class Catalog(models.Model):
    name = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    brand = models.CharField(max_length = 255)
    
    company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name = "catalog")

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    barcode = models.CharField(max_length = 255)
    product_code = models.CharField(max_length = 255)
    
    catalog = models.ForeignKey(Catalog, on_delete = models.CASCADE, related_name = "product")
    company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name = "product")

    def __str__(self):
        return self.name
    