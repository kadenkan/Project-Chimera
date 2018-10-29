import hashlib
from django.db import models


# Create your models here.

class User(models.Model):
    userId = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    hashedPw = models.CharField(max_length=500)
    salt = models.CharField(max_length=100)
