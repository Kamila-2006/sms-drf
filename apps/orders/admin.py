from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'status']
    search_fields = ['status', 'shipping_address', 'notes']