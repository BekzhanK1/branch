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
    # Use MenuItemSerializer for serialization
    menu_item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    # Use OrderItemSerializer for serialization
    order_items = OrderItemSerializer(many = True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_items',
                  'order_time', 'total_price', 'company']
