from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Watchlist, Stock

class UserModelTestCase(TestCase):
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
        """Test lowercase email matches entered email"""
        email = 'tesDFDJFt@test.net'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test invalid email raises ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')


class StockTestCase(TestCase):
    """Test Stock and Watchlist Models"""

    def setUp(self):
        pass

    def test_creating_stock_works(self):
        name = "AAPL"
        Stock.objects.create(name=name)
        self.assertEqual(Stock.objects.get(name="AAPL").name, name)

