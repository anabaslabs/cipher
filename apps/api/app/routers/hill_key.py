import random
import math


def generate_key() -> dict:
    while True:
        matrix = [[random.randint(0, 25) for _ in range(2)] for _ in range(2)]
        det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
        if math.gcd(det, 26) == 1:
            return {"size": 2, "matrix": matrix}