from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from account.models import EmployeePosition, EmployeeUser
from company.serializers import CompanySerializer

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"
        
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
        
#         if instance.is_admin:
#             role = "admin"
#         elif instance.is_employee:
#             role = "employee"
#         elif instance.is_superadmin:
#             role = "superadmin"
            
#         representation['role'] = role

#         return representation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(read_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phonenumber', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class OwnerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(read_only = True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phonenumber', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_owner(password=password, **validated_data)
        return user
    
class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # user_type = serializers.CharField(read_only = True)
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phonenumber']

    def create(self, validated_data):
        
        print(validated_data)
        password = validated_data.pop("password")
        user = User.objects.create_employee(password=password, **validated_data)
        return user

class EmployeePositionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmployeePosition
        fields = ['id', 'name', 'shortname', 'company']

class EmployeeUserSerializer(serializers.ModelSerializer):

    user = EmployeeRegistrationSerializer(read_only = True)
    company = CompanySerializer(read_only = True)
    position = EmployeePositionSerializer(read_only = True)
    start_date = serializers.DateField(read_only = True)

    class Meta:
        model = EmployeeUser
        fields = ['id', 'user', 'position', 'company', 'salary', 'user_id', 'position_id', 'company_id', 'start_date']
        
        extra_kwargs = {
            'user_id': {'source': 'user', 'write_only': True},
            'position_id': {'source': 'position', 'write_only': True},
            'company_id': {'source': 'company', 'write_only': True},
        }