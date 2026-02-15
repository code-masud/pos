from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from .models import Company

User = get_user_model()

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'phone', 'email', 'address']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'username', 'password1', 'password2', 'role', 'branches']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'select2 form-control'
            }),
            'branches': forms.SelectMultiple(attrs={
                'class': 'select2 form-control',
                'multiple': 'multiple',
            })
        }

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'phone', 'email', 'role', 'branches', 'address']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'select2 form-control'
            }),
            'branches': forms.SelectMultiple(attrs={
                'class': 'select2 form-control',
                'multiple': 'multiple',
            }),
        }