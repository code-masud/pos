from django.contrib import admin
from .models import Category, Brand, Product, Stock,StockMovement
from django.utils.html import format_html

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ['id', 'name', 'parent', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['parent', 'is_active']
    list_per_page = 10
    search_fields = ['name', 'parent']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand

    list_display = ['id', 'name', 'description', 'logo',  'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    list_per_page = 10
    search_fields = ['name', 'parent']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ['id','name', 'preview_image', 'sku', 'category', 'selling_price']
    list_display_links = ['id','name',]
    list_filter = ['is_stockable', 'is_active']
    list_per_page = 10
    search_fields = ['name', 'sku', 'category']

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src={} style="width:50px;height=50px;">',
                obj.image.url
            )
        return '--'
    preview_image.short_description = 'Image'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    model = Stock

    list_display = ['id', 'product', 'branch', 'quantity', 'reorder_level']
    list_display_links = ['id', 'product']
    list_filter = ['quantity', 'reorder_level']
    list_per_page = 10
    search_fields = ['product', 'branch']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    model = StockMovement

    list_display = ['id', 'product', 'branch', 'movement_type', 'quantity', 'reference', 'created_by']
    list_display_links = ['id', 'product']
    list_filter = ['created_by', 'movement_type',]
    list_per_page = 10
    search_fields = ['product', 'branch', 'quantity', ]