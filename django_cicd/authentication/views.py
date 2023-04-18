from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db import transaction

from rest_framework import generics
from rest_framework import views
from rest_framework import status 
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_cicd import utils 
from django_cicd.authentication import serializers
from django_cicd import models
from django_cicd.authentication.utils import AuthNotificationFactory

class RegisterView(generics.GenericAPIView):
    '''
    A class that registers a new User
    '''
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.RegisterSerializer
    
    def post(self, request):
        data = request.data 
        serializer_data = self.serializer_class(data=data)
        with transaction.atomic(): 
            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()

                # send email notification and link for account activation
                # user = models.User.objects.get(email=serializer_data.data['email'])
                # token = RefreshToken.for_user(user).access_token
                # domain_name = get_current_site(request).domain
                # abs_path = reverse('verify-email')     
                # mail_response = AuthNotificationFactory().register_email_notification(domain_name,user,token,abs_path)
                # if mail_response.status_code == 202:
                return utils.CustomResponse.Success('Registered Sucessfully', status=status.HTTP_201_CREATED)
            return utils.CustomResponse.Failure(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(views.APIView):
    '''
    A view that verifies a user email and set user.is_verified attribute to True
    '''
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.VerifyEmailSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Input Your Token', type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
            user = models.User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return utils.CustomResponse.Success("Successfully Activated", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return utils.CustomResponse.Failure("Activation Link Expired", status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return utils.CustomResponse.Failure("Invalid Token", status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(generics.GenericAPIView):
    '''
    A view that authenticates a user and return a token
    '''
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.LoginSerializer
    
    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            return utils.CustomResponse.Success(serializer_data.data, status=status.HTTP_200_OK)
        return utils.CustomResponse.Failure(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        