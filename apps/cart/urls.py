from django.urls import path
from . import views


urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('<product_id>/', views.CartView.as_view(), name='remove-product'),
]