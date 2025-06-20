from rest_framework import serializers
from .models import Review
from products.models import Product


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user',  'created_at']

    def create(self, validated_data):
        request = self.context['request']
        product_id = self.context['view'].kwargs.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_id': 'Product does not exist.'})

        validated_data['user'] = request.user
        validated_data['product_id'] = product.id

        return Review.objects.create(
            **validated_data
        )