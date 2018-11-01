from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, userName, email, rawPw, **extra_fields):
        userName = self.normalize_username(userName)
        email = self.normalize_email(email)
        user = self.model(userName=userName, **extra_fields)
        hashedPw = user.make_password(rawPw, None, PBKDF2PasswordHasher)
        user.set_password(hashedPw)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, email, rawPw, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(userName, email, rawPw, **extra_fields)


class User(AbstractBaseUser):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField('user name', max_length=20, unique=True)
    email = models.EmailField('email address', max_length=20)
    password = models.CharField('hashed password', max_length=500)
    salt = models.CharField('salt', max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = []
