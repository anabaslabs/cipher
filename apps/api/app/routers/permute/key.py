import random

ALPHA = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def generate_key() -> str:
    shuffled = ALPHA.copy()
    random.shuffle(shuffled)
    return "".join(shuffled)
