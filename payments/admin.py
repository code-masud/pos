from django.contrib import admin
from .models import PaymentMethod, Payment, Refund

# Register your models here.
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    model = PaymentMethod

    list_display = ['id', 'name', 'code', 'icon', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    list_per_page = 10
    search_fields = ['name', 'code']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    model = Payment

    list_display = ['id',  'sale', 'method', 'amount', 'status', 'processed_by']
    list_display_links = ['id', 'sale']
    list_filter = ['payment_date']
    list_per_page = 10
    search_fields = ['sale', 'method']

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    model = Refund

    list_display = ['id', 'payment', 'amount', 'reason', 'status', 'processed_by']
    list_display_links = ['id', 'payment']
    list_filter = ['status']
    list_per_page = 10
    search_fields = ['reason', 'status']