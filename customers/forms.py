from django import forms
from .models import Customer, CustomerAddress

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'loyalty_points', 'is_active']

class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['customer', 'address', 'city', 'is_default']
        widgets = {
            'customer': forms.Select(attrs={'class': 'select2 form-control'})
        }