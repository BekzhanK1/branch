from rest_framework import serializers
from .models import WarehouseProduct


class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'
