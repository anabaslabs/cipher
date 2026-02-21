import random
import string


def generate_key() -> str:
    length = random.randint(3, 6)
    return "".join(random.choices(string.ascii_uppercase, k=length))
