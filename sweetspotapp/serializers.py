from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
import re
class PasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length
    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(f"The password must be at least {self.min_length} characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValidationError("The password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValidationError("The password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValidationError("The password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+]', value):
            raise ValidationError("The password must contain at least one special character.")
class Customer_serializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[PasswordValidator()])
    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone_no', 'first_name', 'last_name', 'address', 'city', 'state', 'pincode','password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Customer.objects.create_user(password=password, **validated_data)
        return user
class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'
class CakeCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCustomization
        fields ="__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields ='__all__'
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value   
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields ="__all__"