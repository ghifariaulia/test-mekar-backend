from django.test import TestCase
from .models import CustomUser, CustomUserManager

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpassword',
            name='Test User',
            identity_number='123456789',
            date_of_birth='2000-01-01'
        )

    def test_str_method(self):
        self.assertEqual(str(self.user), 'test@example.com')

class CustomUserManagerTests(TestCase):
    def setUp(self):
        self.user_manager = CustomUserManager()

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpassword',
            name='Test User',
            identity_number='123456789',
            date_of_birth='2000-01-01'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.identity_number, '123456789')
        self.assertEqual(user.date_of_birth, '2000-01-01')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='',
                password='testpassword',
                name='Test User',
                identity_number='123456789',
                date_of_birth='2000-01-01'
            )

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword',
            name='Super User',
            identity_number='987654321',
            date_of_birth='1990-01-01'
        )
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertTrue(superuser.check_password('superpassword'))
        self.assertEqual(superuser.name, 'Super User')
        self.assertEqual(superuser.identity_number, '987654321')
        self.assertEqual(superuser.date_of_birth, '1990-01-01')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='superuser@example.com',
                password='superpassword',
                name='Super User',
                identity_number='987654321',
                date_of_birth='1990-01-01',
                is_staff=False
            )

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='superuser@example.com',
                password='superpassword',
                name='Super User',
                identity_number='987654321',
                date_of_birth='1990-01-01',
                is_superuser=False
            )