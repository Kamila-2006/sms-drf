from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderDetailSerializer
from common.pagination import CustomPagination, DetailCustomPagination
from cart.models import CartItem
import random


class OrdersListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    pagination_class = CustomPagination

class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        shipping_address = request.data.get("shipping_address")
        notes = request.data.get("notes", "")

        order = Order.objects.create(
            shipping_address=shipping_address,
            notes=notes,
            status='processing'
        )

        for item in cart_items:
            price = item.product.price
            quantity = item.quantity
            shipping_fee = 5
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=quantity,
                shipping_fee=shipping_fee,
                tracking_number=f'{random.randint(10000000000000000, 99999999999999999)}'
            )

        cart_items.delete()

        serialized_order = OrderDetailSerializer(order).data

        return Response({"success": True, "data": serialized_order}, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    pagination_class = DetailCustomPagination