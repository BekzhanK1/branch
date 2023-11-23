from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.is_admin:
            role = "admin"
        elif instance.is_employee:
            role = "employee"
        elif instance.is_superadmin:
            role = "superadmin"
            
        representation['role'] = role

        return representation


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phonenumber']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phonenumber']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_admin(password=password, **validated_data)
        return user
    
class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phonenumber']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_employee(password=password, **validated_data)
        return user
