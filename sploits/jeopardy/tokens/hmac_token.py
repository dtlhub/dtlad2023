from tokens.token_abstract import Token
import json
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

def pad(data: bytes) -> bytes:
    return data + b'\x00' * (16 - len(data) % 16)

def xor(a: bytes, b: bytes) -> bytes:
    return bytes([i ^ j for i, j in zip(a,b)])

class HmacToken(Token):
    def __init__(self, key: bytes) -> None:
        self.cipher = AES.new(pad(key)[:16], AES.MODE_ECB)

    def __precompute(self, data: bytes) -> bytes:
        data = pad(data)
        hashed = b'\x00' * 16
        for i in range(0, len(data), 16):
            hashed = xor(hashed, data[i: i + 16])

        return hashed

    def generate_token(self, data: bytes) -> str:
        hashed = self.__precompute(data)
        token = f"{b64encode(b'HMAC128').decode()}.{b64encode(data).decode()}.{b64encode(hashed).decode()}"

        return token

    def validate_token(self, token: str) -> bool:
        try:
            token_type, data, signed = list(
                        map(b64decode, token.split('.'))
                    )
        except Exception as e:
            raise Exception('Cannot unpack token')

        if token_type != b'HMAC128':
            return False 

        return self.__precompute(data) == signed
