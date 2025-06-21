from rest_framework import serializers
from .models import CartItem
from products.models import Product


class ProductCartSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'images']

    def get_images(self, obj):
        if obj.images:
            return obj.images.url
        return None

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return round(obj.product.price * obj.quantity, 2)

class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
