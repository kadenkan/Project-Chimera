from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, userName, email, password=None):
        user = self.model(
            userName=userName, 
            email=self.normalize_email(email),
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, email, password=None):
        user = self.create_user(
            userName,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(verbose_name='user name', max_length=20, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=20)

    objects = UserManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
