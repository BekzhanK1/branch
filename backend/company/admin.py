from django.contrib import admin
from company.models import Company, Product, Catalog

# Register your models here.
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Catalog)
# admin.site.register(CompanyEmployee)
