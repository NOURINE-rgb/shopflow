from django.contrib import admin
from .models import OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)
    
@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]