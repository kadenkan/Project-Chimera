from captcha.image import ImageCaptcha
from hashlib import sha256
from django.contrib.auth.hashers import check_password
import random
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

    # def __init__(self, request):
    #     self.chimera_code = {}
    #     self.tempname_list = self.generate_chimera_codes(request)

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

        return tempname

    def generate_chimera_codes(self, request):

        # self.chimera_code.clear()

        temp_name_list = []

        order = random.sample(range(7), 3)

        for i in range(1):

            text_length = range(random.randint(2, 4))

            text = self.create_random_captcha_text(text_length)

            # self.chimera_code[(order[i], text_length)] = self.create_hash(text)

            temp_name_list.append(self.create_image_captcha(request, i, text))

        return temp_name_list

    # def authenticate(self, request, username=None, c_password=None):
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
