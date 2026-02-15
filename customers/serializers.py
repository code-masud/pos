from rest_framework import serializers
from .models import Customer, CustomerAddress

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    addresses = CustomerAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'