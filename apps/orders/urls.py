from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrdersListView.as_view(), name='orders'),
    path('create/', views.OrderCreateView.as_view(), name='create-order'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]