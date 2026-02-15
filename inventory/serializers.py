from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "barcode",
            "description",
            "cost_price",
            "selling_price",
            "discount_price",
            "tax_rate",
            "unit",
            "image",
            "is_active",
            "is_stockable",
            "created_at",
            "updated_at",
            "category",
            "brand",
            "base_price",
            "tax_amount",
            "final_price",
        ]