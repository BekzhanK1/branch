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

        if quantity is None or price_per_unit is None:
            raise serializers.ValidationError("Both quantity and price_per_unit are required.")

        total_price = quantity * price_per_unit
        validated_data['total_price'] = total_price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)
        price_per_unit = validated_data.get('price_per_unit', instance.price_per_unit)

        total_price = quantity * price_per_unit
        validated_data['total_price'] = total_price

        return super().update(instance, validated_data)
