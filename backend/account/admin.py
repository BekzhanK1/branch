from django.contrib import admin

from .models import EmployeePosition, EmployeeUser, CustomerUser
# Register your models here.

admin.site.register(EmployeeUser)
admin.site.register(EmployeePosition)
admin.site.register(CustomerUser)
