# registration/models.py
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models


# class CustomUserManager(BaseUserManager):
#     """
#     Creates and saves a User with the given email, date of
#     birth and password.
#     """
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('User must have an email id')

#         user=self.model(
#             email=self.normalize_email(email)
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None):
#         user=self.create_user(
#             email,
#             password=password
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    # objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    