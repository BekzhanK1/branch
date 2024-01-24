from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

# Create your models here.

class UserType(models.TextChoices):
        
    owner = "owner", "Owner"
    employee = "employee", "Employee"
    customer = "customer", "Customer"
    admin = "admin", "Administrator"

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phonenumber, user_type, password = None):
        if not email:
            raise ValueError("User must have email address")
        
        email = self.normalize_email(email)
        
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            phonenumber = phonenumber,
            user_type = user_type
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    #superadmin@gmail.com qwerty
    def create_superuser(self, email, first_name, last_name, phonenumber, password = None):
        
        user_type = UserType.admin
        
        user = self.create_user(email, first_name, last_name, user_type, phonenumber, password)
        
        
        user.is_staff = True
        user.is_superuser = True
        # user.is_superadmin = True
        user.is_active = True
        
        user.save(using = self._db)
        
        return user
    
    def create_owner(self, email, first_name, last_name, phonenumber, password = None):
        
        user_type = UserType.owner
        
        user = self.create_user(email, first_name, last_name, phonenumber, user_type, password)
        
        user.is_staff = True
        user.is_active = True
        
        user.save(using = self._db)
        
        return user
    
    def create_admin(self, email, first_name, last_name, phonenumber, password = None):
        
        user_type = UserType.admin
        
        user = self.create_user(email, first_name, last_name, phonenumber, user_type, password)
        
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        
        user.save(using = self._db)
        
        return user
    
    def create_employee(self, email, first_name, last_name, phonenumber, password = None):
        
        user_type = UserType.employee
        
        user = self.create_user(email, first_name, last_name, phonenumber, user_type, password)
        
        user.save(using = self._db)
        
        return user
    
    def create_customer(self, email, first_name, last_name, phonenumber, password = None):
        
        user_type = UserType.customer
        
        user = self.create_user(email, first_name, last_name, phonenumber, user_type, password)
        
        user.save(using = self._db)
        
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=25)
    
    
    is_active = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    
    user_type = models.CharField(max_length = 100, choices = UserType.choices)
    
    @property
    def is_owner(self):
        return self.user_type == UserType.owner
    
    @property
    def is_employee(self):
        return self.user_type == UserType.employee
    
    @property
    def is_customer(self):
        return self.user_type == UserType.customer
    
    @property
    def is_admin(self):
        return self.user_type == UserType.admin
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phonenumber"]
    
    def __str__(self):
        return f"{self.email} - {self.user_type}"

class EmployeePosition(models.Model):
    
    name = models.CharField(max_length = 255)
    shortname = models.CharField(max_length = 255)
    company = models.ForeignKey('company.Company', on_delete = models.CASCADE)
    
    def __str__(self):
        
        return self.name
    
class EmployeeUser(models.Model):
        
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "employee")
    position = models.ForeignKey(EmployeePosition, on_delete = models.CASCADE, null = True, blank = True)
    # position = models.CharField(max_length = 100, choices = EmployeePosition.choices, null = True, blank = True)
    company = models.ForeignKey('company.Company', on_delete = models.CASCADE)
    salary = models.FloatField(null = True, blank = True)
    start_date = models.DateField(default = now)
    
    def __str__(self):
        return f"{self.user} - {self.position}"
