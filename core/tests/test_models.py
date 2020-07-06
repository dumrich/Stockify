from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Tests for Core Models"""
    def test_create_user_with_email(self):
        """Test creating user with email"""
        email = 'test@test.net'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password

        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_normalized_email(self):
        email = 'tesDFDJFt@test.net'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
