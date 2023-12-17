from rest_framework import serializers
from .models import WarehouseProduct


class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'
        read_only_fields = ['total_price']

    def create(self, validated_data):
        quantity = validated_data.get('quantity', 0)
        price_per_unit = validated_data.get('price_per_unit', 0)

        total_price = quantity * price_per_unit
        validated_data['total_price'] = total_price
        return super().create(validated_data)
