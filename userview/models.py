
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user
    def create_superuser(self, email, password,**extra_fields):
        """ Create a new superuser profile """
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,null=True)
    is_active = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    
    def __str__(self) :
        return self.first_name
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    
    
    
    