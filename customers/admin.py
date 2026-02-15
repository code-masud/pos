from django.contrib import admin
from .models import Customer, CustomerAddress, LoyaltyTransaction

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer

    list_display = ['id', 'name', 'email', 'phone', 'loyalty_points', 'is_active']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['loyalty_points', 'is_active']
    list_per_page = 10

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    model = CustomerAddress

    list_display = ['id', 'customer', 'address', 'city', 'is_default']
    list_display_links = ['id', 'customer']
    search_fields = ['address', 'city']
    list_filter = ['is_default']
    list_per_page = 10

@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    model = LoyaltyTransaction

    list_display = ['id', 'customer', 'points', 'reference', 'created_at']
    list_display_links = ['id', 'customer']
    search_fields = ['points', 'reference']
    list_filter = ['created_at']
    list_per_page = 10
