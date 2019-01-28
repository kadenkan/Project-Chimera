from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import chimera.settings as settings
import random
from hashlib import sha256
from captcha.image import ImageCaptcha

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


# The number list, lower case character list and upper case character list are used to generate captcha text.
NUMBER_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# PUNCTUATION = ['!', '@', '#', '$', '%', '^', '&',
#                '*', '(', ')', '-', '_', '+', '=', ',', '.', ':']

class Chimera(models.Model):

    # chimera_code = {(start, length), hashing}
    # tempname_list = [name list of the capt imgs]
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=20, default='0.0.0.0')
    chimera_code = models.TextField()
    tempname_list = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

    # This function will create a random captcha string text based on above three list.
    # The input parameter is the captcha text length.

    def create_random_captcha_text(self, text_length):

        base_char = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE + NUMBER_LIST

        # create a 5 char random strin and sha hash it, note that there is no big i
        imgtext = ''.join([random.choice(base_char)
                           for i in range(text_length)])
        # create hash

        return imgtext

    def create_hash(self, captcha_text):

        salt = settings.SECRET_KEY[:20]
        # create hash
        imghash = sha256((salt+captcha_text).encode('utf-8')).hexdigest()

        return imghash

    # Create an image captcha with special text.

    def create_image_captcha(self, request, num, captcha_text):

        image_captcha = ImageCaptcha()
        # Create the captcha image.
        image = image_captcha.generate_image(captcha_text)

        # Add noise curve for the image.
        image_captcha.create_noise_curve(image, image.getcolors())

        # Add noise dots for the image.
        image_captcha.create_noise_dots(image, image.getcolors())

        # Save the image to a png file.
        temp = settings.CAPT_IMAGES_DIR_URL + \
            request.META['REMOTE_ADDR'] + "_" + str(num) + '.png'
        image.save(temp, "PNG")
        tempname = request.META['REMOTE_ADDR'] + "_" + str(num) + '.png'

        self.ip = request.META['REMOTE_ADDR']

        return tempname

    def generate_chimera_codes(self, request):

        self.chimera_code = {}

        self.tempname_list = []

        order = random.sample(range(0, 7), 4)

        for i in range(1, 4):

            text_length = random.randint(2, 4)

            text = self.create_random_captcha_text(text_length)

            self.chimera_code[(order[i], text_length)] = self.create_hash(text)

            self.tempname_list.append((order[i], self.create_image_captcha(request, i, text)))

    
