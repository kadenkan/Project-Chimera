from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.models import PermissionsMixin

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
        superUser = self.create_user(
            userName,
            email,
            password=password,
        )
        superUser.is_admin = True
        superUser.is_staff = True
        superUser.is_superuser = True
        superUser.save(using=self._db)
        return superUser


class User(AbstractBaseUser,PermissionsMixin):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(
        verbose_name='user name', max_length=20, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=20)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.userName

