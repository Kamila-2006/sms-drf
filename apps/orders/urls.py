from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrdersListCreateView.as_view(), name='orders'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]