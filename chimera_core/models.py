from datetime import timedelta
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import chimera.settings as settings
import random
from hashlib import sha256
from PIL import Image, ImageDraw, ImageFont


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


class User(AbstractBaseUser, PermissionsMixin):

    userId = models.AutoField(primary_key=True)

    userName = models.CharField(
        verbose_name='user name', max_length=20, unique=True)

    email = models.EmailField(verbose_name='email address', max_length=20)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    login_dur = models.FloatField(default=0.0)

    objects = UserManager()

    USERNAME_FIELD = 'userName'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.userName


# The number list, lower case character list and upper case character list are used to generate ccode text.
NUMBER_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

SYMBOLS = ['!', '@', '#', '$', '%', '^', '&',
                '*', '(', ')', '-', '_', '+', '=', ',', '.', ':']


class Chimera(models.Model):

    # chimera_code = {(start, end), hashing}
    # tempname_list = [order num, name of the capt imgs]
    id = models.AutoField(primary_key=True)

    ip = models.CharField(max_length=20, default='0.0.0.0')

    chimera_code = models.TextField()

    tempname_list = models.CharField(max_length=100)

    def __str__(self):

        return self.ip

    # This function will create a random ccode string text based on above three list.
    # The input parameter is the ccode text length.

    def create_random_ccode_text(self, text_length):

        base_char = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE + NUMBER_LIST + SYMBOLS

        # create a 5 char random strin and sha hash it, note that there is no big i
        imgtext = ''.join([random.choice(base_char)
                           for i in range(text_length)])
        # create hash

        return imgtext

    def create_hash(self, ccode_text):

        salt = settings.SECRET_KEY[:20]
        # create hash
        imghash = sha256((salt+ccode_text).encode('utf-8')).hexdigest()

        return imghash

    # Create an image ccode with special text.

    def create_image_ccode(self, request, num, ccode_text):

        W, H = (150, 70)

        image = Image.new("RGB", (W, H), (248, 152, 7))

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(settings.STATIC_DIR + "/chimera_core/font/Verdana Pro W01 Light.ttf", 40)

        w, h = draw.textsize(ccode_text, font=font)

        draw.text(((W-w)/2,(H-h)/2), ccode_text, font=font, fill=(255, 255, 255))

        # Save the image to a png file.
        temp = settings.CC_IMAGES_DIR_URL + \
            request.META['REMOTE_ADDR'] + "_" + str(num) + '.png'

        image.save(temp, "PNG")

        tempname = request.META['REMOTE_ADDR'] + "_" + str(num) + '.png'

        self.ip = request.META['REMOTE_ADDR']

        return tempname

    def generate_chimera_codes(self, request):

        self.chimera_code = {}

        self.tempname_list = []

        order = random.sample(range(0, 8), 4)

        order.sort()

        lenadd = 0

        for i in range(3):

            text_length = random.randint(1, 3)

            text = self.create_random_ccode_text(text_length)

            self.chimera_code[(order[i] + lenadd, order[i] +
                               text_length + lenadd)] = self.create_hash(text)

            self.tempname_list.append(
                (order[i], self.create_image_ccode(request, i, text)))

            lenadd += text_length