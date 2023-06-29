from ecdsa_token import EcdsaToken
from hmac_token import HmacToken

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Tokens(metaclass=Singleton):
    def __init__(self) -> None:
        self.token_managers = {
            "EC256": EcdsaToken(b'REDACTED'),
            "HMAC128": HmacToken(b'REDACTED')
        }

    def generate_token(self, message: bytes, type_name: str) -> str:
        return self.token_managers[type_name].generate_token(message)

    def validate_token(self, message: str) -> bool:
        return any(
            [self.token_managers[i].validate_token(message) for i in self.token_managers.keys()]
        )
