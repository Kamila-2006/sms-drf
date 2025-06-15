from rest_framework import generics
from .models import Order
from serializers import OrderListSerializer, OrderDetailSerializer
from common.pagination import CustomPagination, DetailCustomPagination


class OrdersListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    pagination_class = CustomPagination

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    pagination_class = DetailCustomPagination