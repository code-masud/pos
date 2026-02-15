from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

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
    
    @property
    def subtotal_with_tax(self):
        total = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('tax_amount') + F('unit_price'),
                    output_field=DecimalField()
                )
            )
        )['total']

        return total or Decimal('0.00')
    
    @property
    def paid_amount(self):
        total = self.payments.aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')
    
    @property
    def refund_amount(self):
        total = sum(
            (payment.refunded_amount() for payment in self.payments.all()),
            Decimal('0.00')
        )
        return total
    
    @property
    def due_amount(self):
        due = self.total_amount - self.paid_amount - self.refund_amount
        return abs(due)

    @property
    def change_amount(self):
        if self.paid_amount > self.total_amount:
            return self.paid_amount - self.total_amount
        return Decimal('0.00')

    @property
    def payment_methods(self):
        return ", ".join(
            payment.method.name for payment in self.payments.select_related('method')
        )
    
    @property
    def billing_address(self):
        address = self.customer.addresses.filter(is_default=True).first()
        return address.address if address else None

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

