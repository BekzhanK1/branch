from django.contrib import admin

from .models import EmployeePosition, EmployeeUser
# Register your models here.

admin.site.register(EmployeeUser)
admin.site.register(EmployeePosition)
