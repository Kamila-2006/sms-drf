from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductsListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'likes_count']

    def get_likes_count(self):
        return self.likes.count()

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'images', 'category', 'color', 'size', 'material']

    def get_attributes(self, obj):
        return {
            'color': obj.color,
            'size': obj.size,
            'material': obj.material
        }