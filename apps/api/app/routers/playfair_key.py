import random
import string


def generate_key() -> str:
    length = random.randint(4, 8)
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))