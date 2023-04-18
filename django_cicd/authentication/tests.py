from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django_cicd import models

class TestAuthentications(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.register_data = {
            "first_name": "Prosper",
            "last_name": "Ibe",
            "email": "a@a.com",
            "password": "Password1234",
            "phoneNumber": "09021679845",
            "address": "21 Isolo Road",
            "city": "Lagos",
            "lga": "Ikeja",
            "state": "Lagos",
            "user_type": "Proxy"
        }
        self.login_data = {
            "email": "a@a.com",
            "password": "Password1234"
        }
        return super().setUp()
    
    def test_invalid_registration(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_register(self):
        res = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
    def test_login_without_verified_email(self):
        res = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_login_with_verified_email(self):
        res = self.client.post(self.register_url, self.register_data, format='json')
        email = self.register_data['email']
        user = models.User.objects.get(email=email)
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_register_without_email(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            models.User.objects.create_user(password='password123',is_staff=False)

    def test_superuser_creation(self):
        user = models.User.objects.create_superuser(email='a@a.com',password='password123')
        self.assertIsInstance(user,models.User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email,'a@a.com')
    
    def test_create_super_user_with_staff_status(self):
        with self.assertRaisesMessage(ValueError,"Superuser must have is_staff=True."):
            models.User.objects.create_superuser(email='a@a.com',password='password123',is_staff=False)

    def test_create_super_user_with_superuser_status(self):
        with self.assertRaisesMessage(ValueError,"Superuser must have is_superuser=True."):
            models.User.objects.create_superuser(email='a@a.com',password='password123',is_superuser=False)