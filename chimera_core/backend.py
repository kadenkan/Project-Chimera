import random
from hashlib import sha256
from captcha.image import ImageCaptcha
from django.contrib.auth.hashers import check_password
import chimera.settings as settings
from chimera_core.models import User

# The number list, lower case character list and upper case character list are used to generate captcha text.
NUMBER_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# PUNCTUATION = ['!', '@', '#', '$', '%', '^', '&',
#                '*', '(', ')', '-', '_', '+', '=', ',', '.', ':']


class ChimeraAuthBackend:

    # def authenticate(self, request, username=None, cpassword=None):
    #     login_valid = (settings.ADMIN_LOGIN == username)
    #     pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
    #     if login_valid and pwd_valid:
    #         try:
    #             user = User.objects.get(username=username)
    #         except User.DoesNotExist:
    #             # Create a new user. There's no need to set a password
    #             # because only the password from settings.py is checked.
    #             user = User(username=username)
    #             user.is_staff = True
    #             user.is_superuser = True
    #             user.save()
    #         return user
    #     return None

    # def get_user(self, username):
    #     try:
    #         return User.objects.get(pk=username)
    #     except User.DoesNotExist:
    #         return None
    pass