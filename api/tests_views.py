import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        'name': 'Test User',
        'email': 'testuser@email.com',
        'password': '1TestPassword!',
        'identity_number': '12345678901',
        'date_of_birth': '2000-01-01'
    }

@pytest.fixture
def create_user(user_data):
    return CustomUser.objects.create_user(**user_data)

@pytest.mark.django_db
def test_get_user_list(api_client, create_user):
    # Authenticate the client
    token = RefreshToken.for_user(create_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # Get the URL for user list
    url = reverse('users')
    
    # Make the request
    response = api_client.get(url)
    
    # Verify the response
    from .serializers import UserSerializer  # Import here to avoid circular import
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data

@pytest.mark.django_db
def test_get_user_detail(api_client, create_user):
    # Create another user to retrieve
    other_user = CustomUser.objects.create_user(
        email='testuser2@email.com', 
        password='1TestPassword!', 
        name='Test User 2', 
        identity_number='12345678902', 
        date_of_birth='2000-01-01'
    )
    
    # Authenticate the client
    token = RefreshToken.for_user(create_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # Get the URL for user detail
    url = reverse('user', kwargs={'pk': other_user.id})
    
    # Make the request
    response = api_client.get(url)
    
    # Verify the response
    from .serializers import UserSerializer  # Import here to avoid circular import
    serializer = UserSerializer(other_user)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data

@pytest.mark.django_db
def test_update_user_detail(api_client, create_user):
    # Create another user to update
    other_user = CustomUser.objects.create_user(
        email='testuser2@email.com', 
        password='1TestPassword!', 
        name='Test User 2', 
        identity_number='12345678902', 
        date_of_birth='2000-01-01'
    )
    
    # Authenticate the client
    token = RefreshToken.for_user(create_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # Get the URL for user detail
    url = reverse('user', kwargs={'pk': other_user.id})
    
    # Prepare update data
    data = {
        'name': 'Updated Name',
        'email': 'test@email.com',
        'password': '1TestPassword!',
        'identity_number': '12345678903',
        'date_of_birth': '2000-01-01'
    }
    
    # Make the request
    response = api_client.put(url, data)
    
    # Refresh the user from the database
    other_user.refresh_from_db()
    
    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    assert other_user.name == 'Updated Name'

@pytest.mark.django_db
def test_error_put_user(api_client, create_user):
    # Create another user to update
    other_user = CustomUser.objects.create_user(
        email='testuser2@email.com', 
        password='1TestPassword!', 
        name='Test User 2', 
        identity_number='12345678902', 
        date_of_birth='2000-01-01'
    )
    
    # Authenticate the client
    token = RefreshToken.for_user(create_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # Get the URL for user detail
    url = reverse('user', kwargs={'pk': other_user.id})
    
    # Prepare invalid update data
    data = {
        'name': 'Updated Name',
        'email': 'testemail.com',
        'password': '1TestPassword!',
        'identity_number': '12345678903',
        'date_of_birth': '2000-01-01'
    }
    
    # Make the request
    response = api_client.put(url, data)
    
    # Refresh the user from the database
    other_user.refresh_from_db()
    
    # Verify the response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert other_user.name == 'Test User 2'

@pytest.mark.django_db
def test_delete_user(api_client, create_user):
    # Create another user to delete
    other_user = CustomUser.objects.create_user(
        email='testuser2@email.com', 
        password='1TestPassword!', 
        name='Test User 2', 
        identity_number='12345678902', 
        date_of_birth='2000-01-01'
    )
    
    # Authenticate the client
    token = RefreshToken.for_user(create_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # Get the URL for user detail
    url = reverse('user', kwargs={'pk': other_user.id})
    
    # Make the request
    response = api_client.delete(url)
    
    # Verify the response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CustomUser.objects.count() == 1

@pytest.mark.django_db
def test_get_user_id(api_client, create_user):
    # Authenticate the client
    token = RefreshToken.for_user(create_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # Get the URL for getting user ID
    url = reverse('get_user_id')
    
    # Make the request
    response = api_client.get(url)
    
    # Parse the response content
    response_data = json.loads(response.content)
    
    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    assert response_data == {'user_id': create_user.id}

@pytest.mark.django_db
def test_register_user(api_client, user_data):
    # Get the URL for registration
    url = reverse('register')
    
    # Make the request
    response = api_client.post(url, user_data)
    
    # Verify the response
    assert response.status_code == status.HTTP_201_CREATED
    assert CustomUser.objects.count() == 1
    assert CustomUser.objects.get().name == 'Test User'

@pytest.mark.django_db
def test_error_register_user(api_client):
    # Get the URL for registration
    url = reverse('register')
    
    # Make the request with empty data
    response = api_client.post(url, {})
    
    # Verify the response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert CustomUser.objects.count() == 0