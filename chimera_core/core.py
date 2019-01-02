from captcha.image import ImageCaptcha
from hashlib import sha256
import random
import chimera.settings as settings

# The number list, lower case character list and upper case character list are used to generate captcha text.
NUMBER_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# PUNCTUATION = ['!', '@', '#', '$', '%', '^', '&',
#                '*', '(', ')', '-', '_', '+', '=', ',', '.', ':']

class Chimera:

    # This function will create a random captcha string text based on above three list.
    # The input parameter is the captcha text length.

    def create_random_captcha_text(self, text_length):

        base_char = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE + NUMBER_LIST

        # create a 5 char random strin and sha hash it, note that there is no big i
        imgtext = ''.join([random.choice(base_char) for i in range(text_length)])
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
        temp = settings.CAPT_IMAGES_DIR_URL + request.META['REMOTE_ADDR']+ "_" + str(num) + '.png'
        image.save(temp, "PNG")
        tempname = request.META['REMOTE_ADDR'] + "_" + str(num) + '.png'

        return tempname

    def generate_chimera_codes(self, request):

        chimera_code = {}

        order = random.sample(range(8),3)

        for i in range(3):

            text_length = range(random.randint(2, 4))
        
            text = self.create_random_captcha_text(text_length)

            imgname = self.create_image_captcha(request, i, text)

            chimera_code[(order[i],text_length)] = self.create_hash(text)

        return (chimera_code, imgname)



