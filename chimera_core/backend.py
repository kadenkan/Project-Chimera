from django.contrib.auth.hashers import check_password
import chimera.settings as settings
from chimera_core.models import User
import ast
from hashlib import sha256


class ChimeraAuthBackend:

    def authenticate(self, request, chimera=None, username=None, chimerapw=None):

        chimera_code = ast.literal_eval(chimera.chimera_code)

        user = User.objects.get(userName=username)

        password = self.separate(chimera_code, chimerapw)

        if check_password(password, user.password):

            return user

    def get_user(self, username):

        try:

            return User.objects.get(pk=username)

        except User.DoesNotExist:

            return None

    def validate(self, chimera, chimerapw):

        chimera_code = ast.literal_eval(chimera.chimera_code)

        valid = 0

        for key, value in chimera_code.items():

            attempt = chimerapw[key[0]:key[1]]

            salt = settings.SECRET_KEY[:20]

            atthash = sha256((salt+attempt).encode('utf-8')).hexdigest()

            if atthash == value:

                valid += 1

        if valid == 3:

            return True

    def separate(self, chimera_code, chimerapw):

        templs = list(chimerapw)

        positions = sorted(list(chimera_code), key=lambda tup: tup[0])

        for i in positions[::-1]:

            del templs[slice(*i)]

        password = ''.join(templs)

        return password
