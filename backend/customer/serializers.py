from rest_framework import serializers
from .models import Customer, Attendance
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(write_only=True)
    class Meta:
        model = Customer
        fields = '__all__'


    def create(self, validated_data):

        user_email = validated_data.pop('user', None)

        user_instance= User.objects.get(email=user_email)

        customer_instance = Customer.objects.create(user=user_instance, **validated_data)

        return customer_instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = f"{instance.user.first_name} {instance.user.last_name}"
        return representation
    
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'