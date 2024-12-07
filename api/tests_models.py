import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_user():
    CustomUser = get_user_model()
    user = CustomUser.objects.create_user(
        email='test@example.com',
        password='testpassword',
        name='Test User',
        identity_number='123456789',
        date_of_birth='2000-01-01'
    )
    
    assert user.email == 'test@example.com'
    assert user.check_password('testpassword')
    assert user.name == 'Test User'
    assert user.identity_number == '123456789'
    assert user.date_of_birth == '2000-01-01'
    assert user.is_active
    assert not user.is_staff

@pytest.mark.django_db
def test_create_user_without_email():
    CustomUser = get_user_model()
    
    with pytest.raises(ValueError):
        CustomUser.objects.create_user(
            email='',
            password='testpassword',
            name='Test User',
            identity_number='123456789',
            date_of_birth='2000-01-01'
        )

@pytest.mark.django_db
def test_create_superuser():
    CustomUser = get_user_model()
    superuser = CustomUser.objects.create_superuser(
        email='superuser@example.com',
        password='superpassword',
        name='Super User',
        identity_number='987654321',
        date_of_birth='1990-01-01'
    )
    
    assert superuser.email == 'superuser@example.com'
    assert superuser.check_password('superpassword')
    assert superuser.name == 'Super User'
    assert superuser.identity_number == '987654321'
    assert superuser.date_of_birth == '1990-01-01'
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser

@pytest.mark.django_db
def test_create_superuser_without_is_staff():
    CustomUser = get_user_model()
    
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword',
            name='Super User',
            identity_number='987654321',
            date_of_birth='1990-01-01',
            is_staff=False
        )

@pytest.mark.django_db
def test_create_superuser_without_is_superuser():
    CustomUser = get_user_model()
    
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword',
            name='Super User',
            identity_number='987654321',
            date_of_birth='1990-01-01',
            is_superuser=False
        )

@pytest.mark.django_db
def test_user_str_method():
    CustomUser = get_user_model()
    user = CustomUser.objects.create_user(
        email='test@example.com',
        password='testpassword',
        name='Test User',
        identity_number='123456789',
        date_of_birth='2000-01-01'
    )
    
    assert str(user) == 'test@example.com'