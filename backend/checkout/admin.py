from django.contrib import admin
from checkout.models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'external_id', 'abacate_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'external_id', 'abacate_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price')
    search_fields = ('order__external_id', 'product__name')