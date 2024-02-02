from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Customer(models.Model):

    class CustomerStatus(models.TextChoices):
        MEMBER = 'member'
        NEW_CUSTOMER = 'new'
        ACTIVE_CLIENT = 'active_client'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=55, choices=CustomerStatus.choices)
    first_visit = models.DateField(auto_now_add=True)
    last_visit = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} - {self.status}"


class Attendance(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, default = 1)

    def __str__(self) -> str:
        return f"{self.check_in_time}"