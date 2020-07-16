from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Watchlist, Stock

def sample_user(email='test@test.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)

def sample_stock(name='AAPL'):
    return Stock.objects.create(name=name)
class ModelTestCase(TestCase):
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

    def test_superuser_creation(self):
        """Test creating superuser"""
        get_user_model().objects.create_superuser('test@test.com', 'testpass')
        self.assertTrue(get_user_model().objects.get(email='test@test.com').is_superuser)
        self.assertTrue(get_user_model().objects.get(email='test@test.com').is_staff)

    def test_creating_stock_works(self):
        name = "AAPL"
        Stock.objects.create(name=name)
        self.assertEqual(Stock.objects.get(name="AAPL").name, name)

    def test_creating_watchlist(self):
        WatchlistArgs = {'author': sample_user(), 'name':'Watchlist' }
        Watchlist.objects.create(**WatchlistArgs)
        self.assertEqual(Watchlist.objects.get(name='Watchlist').name, WatchlistArgs['name'])
