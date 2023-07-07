from tokens.ecdsa_token import EcdsaToken
from tokens.rc4_token import RC4Token
import json
from base64 import b64decode

class Tokens:
    def __init__(self, iv: bytes = b'dtlad2023') -> None:
        self.token_managers = {
            "EC256": EcdsaToken(b'REDACTED'),
            "ARC228": RC4Token(b'REDACTED', iv = iv)
        }

    def generate_token(self, message: bytes, type_name: str) -> str:
        return self.token_managers[type_name].generate_token(message)

    def validate_token(self, message: str) -> bool:
        return any(
            [self.token_managers[i].validate_token(message) for i in self.token_managers.keys()]
        )

    def get_data(self, message: str) -> dict:
        try:
            token_type, data, signed = list(
                        map(b64decode, message.split('.'))
                    )
        except Exception as e:
            raise Exception('Cannot unpack token')

        return json.loads(data)


