from django.contrib import admin
from company.models import Company, Product, Catalog, Order, OrderItem

# Register your models here.
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Catalog)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(CompanyEmployee)
