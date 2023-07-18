from tokens.token_abstract import Token
from tokens.elliptic.elliptic import ECDSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from base64 import b64encode, b64decode

class EcdsaToken:
    def __init__(self, key) -> None:
        self.signer = ECDSA(key)

    def __precompute(self, data: bytes) -> bytes:
        r, s = self.signer.sign(bytes_to_long(data))
        return f"{r}.{s}".encode()

    def generate_token(self, data: bytes) -> str:
        signature = self.__precompute(data)
        token = f"{b64encode(b'EC256').decode()}.{b64encode(data).decode()}.{b64encode(signature).decode()}"
        return token

    def validate_token(self, token: str) -> bool:
        try:
            token_type, data, signed = list(
                        map(b64decode, token.split('.'))
                    )
        except Exception as e:
            raise Exception('Cannot unpack token')

        if token_type != b'EC256':
            return False
        r, s = list(
            map(int, signed.decode().split('.'))
        )
        return self.signer.validate(bytes_to_long(data), r, s)
