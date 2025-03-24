from re import T
from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product, Category, Collection


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ["name", "slug"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ["name", "slug", "price", "available", "details"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

@admin.register(Collection)
class CollectionAdmin(TranslatableAdmin):
    list_display = ["name", "slug"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}