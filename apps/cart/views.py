from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from products.models import Product
from .serializers import CartItemSerializer, CartAddSerializer
from django.shortcuts import get_object_or_404



class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        serialized_items = CartItemSerializer(items, many=True).data
        total = sum(item['subtotal'] for item in serialized_items)
        items_count = sum(item.quantity for item in items)

        return Response({
            "success": True,
            "data": {
                "items": serialized_items,
                "total": round(total, 2),
                "items_count": items_count
            }
        })

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({"success": True, "message": "Product added to cart"})

    def delete(self, request, product_id):
        cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
        cart_item.delete()

        return Response({"success": True, "message": "Product removed from cart."}, status=status.HTTP_204_NO_CONTENT)