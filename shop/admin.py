from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
    ("Basic Info", {
        "fields": ("category", "name", "slug", "description")
    }),
    ("Image Options", {
        "fields": ("image", "image_url"),
        "description": "Upload image OR paste image URL."
    }),
    ("Pricing & Stock", {
        "fields": ("price", "stock", "is_active")
    }),
)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating",)
