from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager




class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True, null=False)
    phone_no=models.CharField(max_length=11, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects=UserManager()
    REQUIRED_FIELDS=[]
    
  


# Create your models here.
