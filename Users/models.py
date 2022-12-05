from time import timezone
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import MyUserManager

# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField( max_length=30,unique=True)
    first_name = models.CharField( max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email", max_length=60,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class SubscribedUsers(models.Model):
    # name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email