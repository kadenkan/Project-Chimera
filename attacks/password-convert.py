import random
from chimera_core.models import Chimera

def main:
    pwdF = ""


    with open(pwdF) as f:

        content = f.readlines()

        passwords = [x.strip() for x in content] 

    for pwd in passwords:

        result = chimera_insert(pwd)


def chimera_insert(password):

    order = random.sample(range(0, 8), 4).sort()

    lenadd = 0

    for i in order:

        text_length = random.randint(1, 3)

        text = Chimera.create_random_ccode_text(text_length)

        position = i+lenadd

        password = password[position:] + text + password[:position]

        lenadd += text_length

    return password

        
