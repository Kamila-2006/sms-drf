from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
    search_fields = ['user', 'product', 'rating', 'comment']