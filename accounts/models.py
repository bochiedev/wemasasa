from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from .constants import TYPE
from .manager import CustomUserManager



class User(AbstractUser):
    email = models.EmailField(unique=True,max_length=255)
    member_no = models.CharField(unique=True, max_length=255)
    type = models.CharField(choices=TYPE, max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email + " " +self.member_no
    