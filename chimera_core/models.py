from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, userName, email, rawPw, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userId = models.IntegerField(primary_key=True)
    userName = models.CharField('user name', max_length=20, unique=True)
    email = models.EmailField('email address', max_length=20)
    hashedPw = models.CharField('hashed password', max_length=500)
    salt = models.CharField('salt', max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = []


