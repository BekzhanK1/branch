from rest_framework import serializers
from .models import Company, Catalog, Product, Order, OrderItem
from menu.serializers import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(many=True)  # Use MenuItemSerializer for serialization

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # Use OrderItemSerializer for serialization

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'order_time', 'total_price', 'company']
