import binascii
import base64
import struct


class RC5:
    def __init__(self, key_bytes, w=32, r=12):
        self.w = w
        self.r = r
        self.b = len(key_bytes)
        self.mod = 2**self.w
        self.mask = self.mod - 1
        self.S = self._key_expand(key_bytes)
        
        if self.w == 16:
            self.pack_fmt = '<2H'
        elif self.w == 32:
            self.pack_fmt = '<2I'
        elif self.w == 64:
            self.pack_fmt = '<2Q'
        else:
            self.pack_fmt = None
            
        self.block_size = 2 * (self.w // 8)

    def _lshift(self, val, n):
        n %= self.w
        return ((val << n) & self.mask) | (val >> (self.w - n))

    def _key_expand(self, K):
        if len(K) == 0:
            K = b'\x00'
            
        u = self.w // 8
        c = max(1, (len(K) + u - 1) // u)
        L = [0] * c
        for i in range(len(K)):
            L[i // u] += K[i] << (8 * (i % u))

        if self.w == 16:
            P, Q = 0xB7E1, 0x9E37
        elif self.w == 32:
            P, Q = 0xB7E15163, 0x9E3779B9
        elif self.w == 64:
            P, Q = 0xB7E151628AED2A6B, 0x9E3779B97F4A7C15
        else:
            P, Q = 0xB7E15163, 0x9E3779B9

        t = 2 * (self.r + 1)
        S = [0] * t
        S[0] = P
        for i in range(1, t):
            S[i] = (S[i-1] + Q) & self.mask

        i = j = A = B = 0
        for _ in range(3 * max(len(L), t)):
            A = S[i] = self._lshift((S[i] + A + B) & self.mask, 3)
            B = L[j] = self._lshift((L[j] + A + B) & self.mask, (A + B))
            i = (i + 1) % t
            j = (j + 1) % len(L)
        return S

    def decrypt_data(self, ciphertext):
        if not self.pack_fmt:
            raise ValueError(f"Unsupported word size: {self.w}. Use 16, 32, or 64.")
            
        out = bytearray(len(ciphertext))
        S = self.S
        r = self.r
        mask = self.mask
        w = self.w
        unpack = struct.unpack_from
        pack = struct.pack_into
        fmt = self.pack_fmt
        block_size = self.block_size
        
        for offset in range(0, len(ciphertext), block_size):
            A, B = unpack(fmt, ciphertext, offset)
            
            for i in range(r, 0, -1):
                val = (B - S[2 * i + 1]) & mask
                n = A % w
                B = (((val >> n) | (val << (w - n))) & mask) ^ A
                
                val = (A - S[2 * i]) & mask
                n = B % w
                A = (((val >> n) | (val << (w - n))) & mask) ^ B
                
            B = (B - S[1]) & mask
            A = (A - S[0]) & mask
            
            pack(fmt, out, offset, A, B)
        return bytes(out)


def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]


def decrypt(b64_ciphertext: str, hex_key: str, w: int = 32, r: int = 12) -> dict:
    if w not in (16, 32, 64):
        raise ValueError("Word size (w) must be 16, 32, or 64 bits.")
    if not (0 <= r <= 255):
        raise ValueError("Rounds (r) must be between 0 and 255.")

    key_bytes = binascii.unhexlify(hex_key)
    ciphertext = base64.b64decode(b64_ciphertext)
    rc5 = RC5(key_bytes, w=w, r=r)
    
    padded_plaintext = rc5.decrypt_data(ciphertext)

    plaintext = unpad(padded_plaintext).decode("utf-8")

    return {
        "key": hex_key,
        "plaintext": plaintext
    }