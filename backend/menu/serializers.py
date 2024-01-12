from datetime import timedelta
from rest_framework import serializers
from .models import Category, MenuItem


class DurationStringField(serializers.Field):
    def to_representation(self, value):
        # Convert the duration to a string in the format "mm:ss"
        minutes, seconds = divmod(value.seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def to_internal_value(self, data):
        # Parse the string in the format "mm:ss" back to a Duration object
        try:
            minutes, seconds = map(int, data.split(':'))
            return timedelta(minutes=minutes, seconds=seconds)
        except (ValueError, AttributeError):
            raise serializers.ValidationError(
                "Invalid duration format. Use 'mm:ss'.")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    preparation_time = DurationStringField()

    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['popularity']

    def create(self, validated_data):
        price = validated_data.get('price', 0)

        if price is None:
            raise serializers.ValidationError('Price should be set')

        return MenuItem.objects.create(**validated_data)
