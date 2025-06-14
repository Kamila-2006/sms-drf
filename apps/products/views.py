from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from django_filters import rest_framework as filters
from .models import Product, Like
from .serializers import ProductDetailSerializer, ProductsListSerializer
from apps.common.pagination import CustomPagination, DetailCustomPagination


# class ProductFilter(filters.FilterSet):
#     category = filters.NumberFilter(field_name="category__id", lookup_expr="exact")  # Фильтрация по категории
#     min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")  # Фильтрация по минимальной цене
#     max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")  # Фильтрация по максимальной цене
#     attributes = filters.CharFilter(field_name="attributes", method="filter_by_attributes")  # Фильтрация по атрибутам
#     search = filters.CharFilter(field_name="title", lookup_expr="icontains")  # Поиск по названию
#     sort = filters.OrderingFilter(fields=['price', 'created_at', 'title', 'rating'])  # Сортировка
#     order = filters.OrderingFilter(fields=['price', 'created_at', 'title', 'rating'], default=['price'], ordering=True)  # Порядок сортировки
#
#     class Meta:
#         model = Product
#         fields = ['category', 'min_price', 'max_price', 'attributes', 'search', 'sort', 'order']

    # def filter_by_attributes(self, queryset, name, value):
    #     import json
    #     try:
    #         attributes = json.loads(value)
    #     except ValueError:
    #         return queryset
    #     for key, val in attributes.items():
    #         queryset = queryset.filter(**{f"{key}__iexact": val})
    #     return queryset

class ProductsListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    # filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    # filterset_class = ProductFilter

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DetailCustomPagination

class ProductReactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        value = request.data.get("value")

        if value not in ["like", "dislike"]:
            return Response({"error": "Invalid value. Use 'like' or 'dislike'."}, status=400)

        like, created = Like.objects.get_or_create(user=request.user, product=product)

        if not created:
            if like.value == value:
                like.delete()
                return Response({"message": "Reaction removed"}, status=200)
            else:
                like.value = value
                like.save()
                return Response({"message": f"Reaction changed to {value}"}, status=200)

        return Response({"message": f"{value} added"}, status=201)