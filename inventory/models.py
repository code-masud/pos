from django.db import models
from services.uploads import product_image_upload_path, logo_upload_path
from services.validations import image_validation
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy
from django.conf import settings
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to=logo_upload_path, validators=[image_validation], blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('box', 'Box'),
        ('pack', 'Pack'),
    ]
    
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    # Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text='percentage (e.g. 5.00)')
    
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pcs')
    image = models.ImageField(upload_to=product_image_upload_path, validators=[image_validation], null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_stockable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def base_price(self):
        return self.discount_price if self.discount_price else self.selling_price

    @property
    def tax_amount(self):
        return (self.base_price * self.tax_rate) / Decimal("100")

    @property
    def final_price(self):
        return self.base_price + self.tax_amount
    
    def __str__(self):
        return f"{self.name} ({self.sku})"

class Stock(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name="stocks")
    branch = models.ForeignKey("accounts.Branch",on_delete=models.PROTECT,related_name="stocks")
    quantity = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    reorder_level = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.branch}"

class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJ"
    TRANSFER = "TRF"

    MOVEMENT_TYPES = [
        (IN, "Stock In"),
        (OUT, "Stock Out"),
        (ADJUSTMENT, "Adjustment"),
        (TRANSFER, "Transfer"),
    ]

    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    branch = models.ForeignKey("accounts.Branch",on_delete=models.PROTECT)
    movement_type = models.CharField(max_length=3,choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    reference = models.CharField(max_length=100,blank=True, help_text='sale id, purchase id, adjustment reason')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product}"