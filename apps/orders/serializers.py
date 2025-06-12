from rest_framework import serializers
from .models import Order


class OrderDetailSerializer(serializers.ModelSerializer):
    order_number = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'created_at', 'updated_at', 'status', 'shipping_address', 'notes']

    def get_order_number(self, obj):
        return f'ORD - {obj.id}'
