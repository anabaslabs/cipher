import binascii
import base64


class RC5:
    def __init__(self, key_bytes):
        self.w = 32
        self.r = 12
        self.b = 16
        self.mod = 2**32
        self.S = self._key_expand(key_bytes)

    def _lshift(self, val, n):
        n %= self.w
        return ((val << n) & (self.mod - 1)) | (val >> (self.w - n))

    def _key_expand(self, K):
        L = [int.from_bytes(K[i*4:(i+1)*4], byteorder='little') for i in range(len(K)//4)]
        P32, Q32 = 0xB7E15163, 0x9E3779B9
        t = 2 * (self.r + 1)
        S = [0] * t
        S[0] = P32
        for i in range(1, t):
            S[i] = (S[i-1] + Q32) & (self.mod - 1)

        i = j = A = B = 0
        for _ in range(3 * max(len(L), t)):
            A = S[i] = self._lshift((S[i] + A + B) & (self.mod - 1), 3)
            B = L[j] = self._lshift((L[j] + A + B) & (self.mod - 1), (A + B))
            i = (i + 1) % t
            j = (j + 1) % len(L)
        return S

    def encrypt_block(self, data):
        A = int.from_bytes(data[:4], byteorder='little')
        B = int.from_bytes(data[4:], byteorder='little')
        A = (A + self.S[0]) & (self.mod - 1)
        B = (B + self.S[1]) & (self.mod - 1)
        for i in range(1, self.r + 1):
            A = (self._lshift(A ^ B, B) + self.S[2 * i]) & (self.mod - 1)
            B = (self._lshift(B ^ A, A) + self.S[2 * i + 1]) & (self.mod - 1)
        return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')


def pad(data):
    padding_len = 8 - (len(data) % 8)
    return data + bytes([padding_len] * padding_len)


def encrypt(plaintext: str, hex_key: str) -> dict:
    key_bytes = binascii.unhexlify(hex_key)
    if len(key_bytes) != 16:
        raise ValueError("Key must be 32 hex characters (16 bytes).")

    rc5 = RC5(key_bytes)
    padded_data = pad(plaintext.encode("utf-8"))
    ciphertext = b''

    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i+8]
        ciphertext += rc5.encrypt_block(block)

    b64_ciphertext = base64.b64encode(ciphertext).decode("utf-8")

    return {
        "key": hex_key,
        "ciphertext": b64_ciphertext
    }