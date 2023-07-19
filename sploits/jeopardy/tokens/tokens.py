from tokens.ecdsa_token import EcdsaToken
from tokens.rc4_token import RC4Token
from tokens.token_abstract import Token
from hashlib import md5
import json
from base64 import b64decode

class Tokens(Token):
    def __init__(self, key:bytes = b'REDACTED', iv: bytes = b'dtlad2023') -> None:
        self.token_managers = {
            "EC256": EcdsaToken(key),
            "ARC228": RC4Token(key, iv = iv)
        }

    def generate_token(self, message: bytes, type_name: str) -> str:
        return self.token_managers[type_name].generate_token(md5(message).digest())

    def validate_token(self, message: str) -> bool:
        return any(
            [self.token_managers[i].validate_token(md5(message.encode()).digest()) for i in self.token_managers.keys()]
        )

    def get_signed(self, message: str) -> dict:
        try:
            token_type, data, signed = list(
                        map(b64decode, message.split('.'))
                    )
        except Exception as e:
            raise Exception('Cannot unpack token')

        return signed
