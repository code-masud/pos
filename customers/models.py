from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20,unique=True,blank=True,null=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    loyalty_points = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="addresses")
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)

class LoyaltyTransaction(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,related_name="loyalty_transactions")
    points = models.DecimalField(max_digits=10,decimal_places=2)
    reference = models.CharField(max_length=100, help_text="sale / refund id")
    created_at = models.DateTimeField(auto_now_add=True)
