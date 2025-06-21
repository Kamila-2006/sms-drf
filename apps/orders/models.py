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

    order_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def subtotal(self):
        return round(sum(item.subtotal() for item in self.items.all()), 2)

    def total(self):
        return self.subtotal() + sum(item.shipping_fee for item in self.items.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    shipping_fee = models.PositiveIntegerField()
    tracking_number = models.CharField(max_length=18)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    def subtotal(self):
        return self.product.price * self.quantity