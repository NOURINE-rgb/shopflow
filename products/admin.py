from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "category",
        "stock",
        "is_hot",
        "is_limited",
        "discounted_price",
        "created_at",
    )
    list_filter = ("category", "is_hot", "is_limited", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
