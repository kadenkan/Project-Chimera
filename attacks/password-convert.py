import random
import codecs

NUMBER_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

SYMBOLS = ['!', '@', '#', '$', '%', '^', '&',
                '*', '(', ')', '-', '_', '+', '=', ',', '.', ':']

def chimera_insert(password):

    order = random.sample(range(0, 8), 3)

    order.sort()

    lenadd = 0

    for i in order:

        text_length = random.randint(1, 3)

        base_char = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE + NUMBER_LIST + SYMBOLS

        text = ''.join([random.choice(base_char)for i in range(text_length)])

        position = i+lenadd

        password = password[:position] + text + password[position:]

        lenadd += text_length

    return password

with codecs.open("attacks/ry-extracted.txt", 'r',encoding='utf8') as sf, codecs.open("attacks/ry-extracted-cp.txt", 'w',encoding='utf8') as rf:

    content = sf.readlines()

    passwords = [x.strip() for x in content] 

    for pwd in passwords:

        if len(pwd) >= 8:

            result = chimera_insert(pwd)

            rf.write(result+"\n")

            result = ''
    
    print("Finished.")


# with open("attacks/rockyou.txt", 'w',encoding ='utf8') as f:
#     for pwd in passwords:
#         if len(pwd) >= 8:
#             f.write(pwd+"\n")
