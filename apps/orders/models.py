from django.db import models


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
    status = models.CharField(max_length='20', choices=STATUS_CHOICES)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    
class OrderItem(models.Model):
    pass