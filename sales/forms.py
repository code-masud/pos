from django import forms
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['receipt_number', 'branch', 'cashier', 'customer', 'subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'status', 'notes', 'completed_at']

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['sale', 'product', 'quantity', 'unit_price', 'tax_rate', 'tax_amount', 'total_price']