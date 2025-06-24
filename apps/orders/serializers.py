from rest_framework import serializers

from cart.serializers import ProductCartSerializer
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
    product = ProductCartSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'shipping_fee', 'tracking_number']

    def get_subtotal(self, obj):
        return obj.subtotal()

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'created_at', 'updated_at', 'status', 'shipping_address', 'notes', 'items']

    def get_subtotal(self, obj):
        return obj.subtotal()

    def get_total(self, obj):
        return obj.total()