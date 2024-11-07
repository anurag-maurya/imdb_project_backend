from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist.models import StreamPlatform

# Create your tests here.

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Passowrd@123")
        self.user.is_staff = True 
        # only admin has permission to create stream so making this user staff
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = StreamPlatform.objects.create(name="netflix", about="netflix stream",
                                                    website="https://www.netflix.com")
        
    
    def test_stream_list(self):
        response=self.client.get(reverse("stream-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_stream_create(self):
        data = {
            "name": "prime",
            "about": "amazon prime",
            "website": "https://www.prime.com/"
        }
        response = self.client.post(reverse("stream-list"),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_stream_detail(self):
        response = self.client.get(reverse("stream-detail", args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_stream_update(self):
        data = {
            "name": "netflix updated",
            "about": "netflix stream",
            "website": "https://www.netflix.com/"
        }
        response = self.client.put(reverse("stream-detail", args=(self.stream.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_stream_delete(self):
        response = self.client.delete(reverse("stream-detail", args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    
