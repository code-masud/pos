from django import forms
from .models import PaymentMethod, Payment, Refund

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'code', 'icon', 'is_active']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['number', 'sale', 'method', 'amount', 'status', 'processed_by', 'payment_date', 'notes']
        widgets = {
            'sale': forms.Select(attrs={'class': 'select2 form-control'}),
            'method': forms.Select(attrs={'class': 'select2 form-control'}),
            'processed_by': forms.Select(attrs={'class': 'select2 form-control'}),
        }

class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['number', 'payment', 'sale', 'amount', 'reason', 'status', 'processed_by']
        widgets = {
            'payment': forms.Select(attrs={'class': 'select2 form-control'}),
            'sale': forms.Select(attrs={'class': 'select2 form-control'}),
            'processed_by': forms.Select(attrs={'class': 'select2 form-control'}),
        }