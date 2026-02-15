from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Sale(models.Model):
    DRAFT = "DRAFT"
    COMPLETED = "COMPLETED"
    VOIDED = "VOIDED"
    REFUNDED = "REFUNDED"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (COMPLETED, "Completed"),
        (VOIDED, "Voided"),
        (REFUNDED, "Refunded"),
    ]

    receipt_number = models.CharField(max_length=30,unique=True,null=True,blank=True)
    branch = models.ForeignKey("accounts.Branch",on_delete=models.PROTECT,related_name="sales")

    cashier = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="sales")
    customer = models.ForeignKey("customers.Customer",on_delete=models.SET_NULL,null=True,blank=True)

    subtotal = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    tax_amount = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    discount_amount = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_amount = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=DRAFT)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.receipt_number

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey("inventory.Product",on_delete=models.PROTECT)

    quantity = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    unit_price = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    tax_rate = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    tax_amount = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_price = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return f"{self.product} x {self.quantity}"

