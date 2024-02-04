from rest_framework import serializers
from .models import Company, Catalog, Product, Order, OrderItem
from menu.serializers import *
# from account.serializers import UserSerializer

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
    menu_item = MenuItemSerializer(read_only = True)
    menu_item_id = serializers.IntegerField(write_only = True)
    order_id = serializers.IntegerField(write_only = True)
    
    subtotal = serializers.DecimalField(read_only = True, max_digits=10, decimal_places=2)


    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'order_id', 'menu_item', 'quantity', 'subtotal', 'menu_item_id']
        
        read_only_fields = ['order']
        extra_kwargs = {
            'menu_item_id': {'source': 'menu_item', 'write_only': True},
            'order_id': {'source': 'order', 'write_only': True}
        }
        
    def create(self, validated_data):
        
        menu_item_id = validated_data.pop("menu_item_id")
        order_id = validated_data.pop("order_id")
        
        menu_item = MenuItem.objects.get(pk = menu_item_id)
        order = Order.objects.get(pk = order_id)
        
        subtotal = menu_item.price * validated_data['quantity']
        
        order_item = OrderItem.objects.create(
            order = order,
            menu_item = menu_item,
            quantity = validated_data['quantity'],
            subtotal = subtotal
        )
        
        return order_item
        
        
        
        

class OrderItemWriteSerializer(serializers.Serializer):
    
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # subtotal = serializers.FloatField()

class OrderSerializer(serializers.ModelSerializer):
    # Use OrderItemSerializer for serialization
    order_items = OrderItemSerializer(read_only = True, many = True, source='orderitem_set')
    items = OrderItemWriteSerializer(write_only = True, many = True)
    
    order_time = serializers.DateTimeField(read_only = True)
    total_price = serializers.DecimalField(read_only = True, max_digits=10, decimal_places=2)
    
    company_id = serializers.IntegerField(write_only = True)
    company = CompanySerializer(read_only = True)
    
    customer_id = serializers.IntegerField(write_only = True)
    # customer = serializers.IntegerField(read_only = True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_items', 'items',
                  'order_time', 'total_price', 'company', 'company_id', 'customer_id']
        
        read_only_fields = ['customer']
        
        extra_kwargs = {
            'company_id': {'source': 'company', 'write_only': True},
            'customer_id': {'source': 'customer', 'write_only': True},
        }
        
    def create(self, validated_data):
        
        
        items = validated_data.pop("items")
        
        print(validated_data)
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        for item in items:
            
            order_dict = {
                "menu_item_id": item['menu_item_id'],
                'order_id': order.id,
                "quantity": item['quantity']
            }
            
            item_serializer = OrderItemSerializer(data = order_dict)
            
            if item_serializer.is_valid():
                item_serializer.save()
                
                print(item_serializer.data)
                total_price += float(item_serializer.data['subtotal'])
            else:
                order.delete()
                raise serializers.ValidationError(item_serializer.errors)
        
        order.total_price = total_price
        order.save()
        
        return order
