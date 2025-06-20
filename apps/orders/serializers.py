from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderListSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    order_number = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'created_at', 'status', 'items_count']

    def get_items_count(self, obj):
        return obj.items.count()

    def get_order_number(self, obj):
        return f"ORD-{obj.id}"

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'shipping_fee', 'tracking_number']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer()

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'created_at', 'updated_at', 'status', 'shipping_address', 'notes', 'items']