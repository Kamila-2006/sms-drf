from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Like
from .serializers import ProductDetailSerializer, ProductsListSerializer
from common.pagination import CustomPagination, DetailCustomPagination


class ProductsListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

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