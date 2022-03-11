import random
import string


def generate_identificator():
    letters = string.ascii_letters
    digits = string.digits
    chars = letters + digits
    identificator = "".join([random.choice(chars) for i in range(12)])
    return identificator
