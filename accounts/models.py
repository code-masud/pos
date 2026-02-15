from django.contrib.auth.models import AbstractUser
from django.db import models
from services.validations import image_validation
from services.uploads import logo_upload_path, avatar_upload_path

class Company(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField()
    tax_id = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=logo_upload_path, validators=[image_validation], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Branch(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('staff', 'Staff'),
    ]
    
    email = models.EmailField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to=avatar_upload_path, validators=[image_validation], blank=True, null=True)
    branches = models.ManyToManyField(Branch, related_name="users", blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

