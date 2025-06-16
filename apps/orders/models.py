from django.db import models
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    shipping_fee = models.PositiveIntegerField()
    tracking_number = models.CharField(max_length=18)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')