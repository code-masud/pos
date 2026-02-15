from django import forms
from .models import Category, Brand, Product, Stock, StockMovement

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'is_active']
        widgets = {
            'parent': forms.Select(attrs={'class': 'select2 form-control'})
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo', 'is_active']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'sku', 'barcode', 'category', 'brand', 'unit', 'cost_price', 'selling_price', 'discount_price', 'tax_rate', 'is_active', 'is_stockable']
        widgets = {
            'category': forms.Select(attrs={'class': 'select2 form-control'}),
            'brand': forms.Select(attrs={'class': 'select2 form-control'}),
            'unit': forms.Select(attrs={'class': 'select2 form-control'}),
        }
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product', 'branch', 'quantity', 'reorder_level']

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'branch', 'movement_type', 'quantity', 'reference', 'created_by']
