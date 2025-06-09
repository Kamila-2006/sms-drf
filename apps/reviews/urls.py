from django.urls import path,include
from . import views


urlpatterns =  [
    path('products/<int:product_id>/review/', views.ReviewCreateView.as_view(), name='create-review'),
]