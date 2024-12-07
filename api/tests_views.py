import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testuser@email.com', password='1TestPassword!', name='Test User', identity_number='12345678901', date_of_birth='2000-01-01')
        self.url = reverse('users')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_user_list(self):
        response = self.client.get(self.url)
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class UserDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testuser@email.com', password='1TestPassword!', name='Test User', identity_number='12345678901', date_of_birth='2000-01-01')
        self.other_user = CustomUser.objects.create_user(email='testuser2@email.com', password='1TestPassword!', name='Test User 2', identity_number='12345678902', date_of_birth='2000-01-01')
        self.url = reverse('user', kwargs={'pk': self.other_user.id})
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_user_detail(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(self.other_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_user_detail(self):
        data = {
            'name': 'Updated Name',
            'email': 'test@email.com',
            'password': '1TestPassword!',
            'identity_number': '12345678903',
            'date_of_birth': '2000-01-01'
        }
        response = self.client.put(self.url, data)
        self.other_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.other_user.name, 'Updated Name')
    
    def test_error_put_user(self):
        data = {
            'name': 'Updated Name',
            'email': 'testemail.com',
            'password': '1TestPassword!',
            'identity_number': '12345678903',
            'date_of_birth': '2000-01-01'
        }
        response = self.client.put(self.url, data)
        self.other_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.other_user.name, 'Test User 2')
    
    def test_delete_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 1)


class GetUserIdTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testuser@email.com', password='1TestPassword!', name='Test User', identity_number='12345678901', date_of_birth='2000-01-01')
        self.url = reverse('get_user_id')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_user_id(self):
        response = self.client.get(self.url)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {'user_id': self.user.id})

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.data = {
            'name': 'Test User',
            'email': 'testuser@email.com',
            'password': '1TestPassword!',
            'identity_number': '12345678901',
            'date_of_birth': '2000-01-01'
        }

    def test_register_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().name, 'Test User')
    
    def test_error_register_user(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)