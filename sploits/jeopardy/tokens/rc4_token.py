from tokens.token_abstract import Token
from Crypto.Cipher import ARC4
from base64 import b64encode, b64decode

class RC4Token(Token):
    def __init__(self, key: bytes, iv: bytes = b'dtlad2023'):
        self.key = iv + key

    def __precompute(self, data: bytes) -> bytes:
        cipher = ARC4.new(self.key)
        return cipher.decrypt(data)

    def generate_token(self, data: bytes) -> str:
        hashed = self.__precompute(data)
        token = f"{b64encode(b'ARC228').decode()}.{b64encode(data).decode()}.{b64encode(hashed).decode()}"

        return token

    def validate_token(self, token: str) -> bool:
        try:
            token_type, data, signed = list(
                        map(b64decode, token.split('.'))
                    )
        except Exception as e:
            raise Exception('Cannot unpack token')

        if token_type != b'ARC228':
            return False

        return self.__precompute(data) == signed
