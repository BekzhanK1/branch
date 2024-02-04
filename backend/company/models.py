from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from customer.models import Customer
from menu.models import MenuItem

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
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null = True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.first_name} {self.customer.user.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='menu_item')
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity} units"