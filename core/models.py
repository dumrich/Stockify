#Django Core Models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Creates and saves new user"""
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=email.lower())

        user.set_password(password)
        user.save()

        return user
    def create_superuser(self, email, password=None):
        """Creates and saves new Superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

class Stock(models.Model):
    name = models.CharField(max_length=5, unique=True)


    def __str__(self):
        return self.name

class Watchlist(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ManyToManyField(Stock)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']



