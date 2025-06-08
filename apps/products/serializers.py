from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductsListSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    likes_count = serializers.SerializerMethodField()
    # average_rating =

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'images', 'category', 'likes_count']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        return rep

    # def get_average_rating(self, obj):
    #     ratings = obj.reviews.all()
    #     if ratings:
    #         return sum(rating.score for rating in ratings) / len(ratings)
    #     return 0

    def get_likes_count(self, obj):
        return obj.likes.count()


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'images', 'category', 'attributes']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        return rep

    def get_attributes(self, obj):
        return {
            'color': obj.color,
            'size': obj.size,
            'material': obj.material
        }