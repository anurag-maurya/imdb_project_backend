from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


# Create your tests here.

class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username": "test",
            "email": "test@testing.com",
            "password": "Password@123",
            "password2": "Password@123"
        }
        response = self.client.post(reverse('register'),data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="example", password="Passowrd@123")
        self.token = Token.objects.create(user=self.user)
        
    def test_login(self):
        data ={
            "username": "example",
            "password": "Passowrd@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response  = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)






