from django.contrib import admin
from .models import Sale, SaleItem

# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    model = Sale

    list_display = ['id', 'branch', 'cashier', 'customer', 'total_amount', 'status']
    list_display_links = ['id', 'branch']
    list_filter = ['completed_at']
    list_per_page = 10
    search_fields = ['customer', 'branch']

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    model = SaleItem

    list_display = ['id',  'sale', 'product', 'quantity', 'total_price']
    list_display_links = ['id', 'sale']
    list_filter = ['sale']
    list_per_page = 10
    search_fields = ['sale', 'product']