from dataclasses import fields
from rest_framework import serializers 
from .models import Category, Order, OrderedProduct, Product, User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length = 222)
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    username = serializers.CharField(max_length = 68, min_length = 6)
    tokens = serializers.CharField(max_length = 68, read_only = True)

    class Meta:
        model = User
        fields = ['email','password','username','tokens']

    def validate(self, attrs):
        e_mail = attrs.get('email','')
        pswd = attrs.get('password','')
        user = auth.authenticate(email = e_mail, password = pswd)
    
        if not user:
            raise AuthenticationFailed('invalid credantials, try again')
        elif not user.is_active:
            raise AuthenticationFailed('Account dissabled, contact admin')
        elif not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return{
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens
        },super().validate(attrs)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        model = User
        model = Category
        fields = ['name', 'description']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['__all__']

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['__all__']

class OrderedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderedProduct
        fields = ['__all__']