from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers 
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django_cicd import models 
from . import utils

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = models.User 
        fields = ['id','first_name','last_name','email','password','phoneNumber','address','city','lga','state','user_type']
        
    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)
    
    class Meta:
        model = models.User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(min_length=6, write_only=True)
    tokens = serializers.DictField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.User
        fields = ['email','user','password','tokens']
        
    def get_user(self, obj):
        try:
            access_type = models.User.objects.get(email=obj['email'])
            user = {
                "id": access_type.id,
                "first_name": access_type.first_name,
                "last_name": access_type.last_name,
                "phoneNumber": access_type.phoneNumber,
                "address": access_type.address,
                "city": access_type.city,
                "lga": access_type.lga,
                "state": access_type.state,
                "user_type": access_type.user_type,
                "is_verified": access_type.is_verified,
                "is_updated": access_type.is_updated
            }
        except:
            user = {}
        return user
    
    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid Login Credentials")
        if not user.is_verified:
            raise AuthenticationFailed("Email is Not Verified")
        if not user.is_active:
            raise AuthenticationFailed("Account Disabled, Contact the Administrator")
        
        return {
            'email': user.email,
            'tokens': user.tokens
        }