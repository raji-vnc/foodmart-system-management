from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,Brand,Product,CartItem,Order,OrderItem,Payment,Like,Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    brand=BrandSerializer(read_only=True)

    class Meta:
        model=Product
        fields='__all__'

class cartItemSerializer(serializers.ModelSerializer):
    Product=ProductSerializer(read_only=True)
    class Meta:
        model=CartItem
        fields='__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields='__all__'


class PaymentSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)

    class Meta:
        model=Payment
        fields='__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields='__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields='__all__'


