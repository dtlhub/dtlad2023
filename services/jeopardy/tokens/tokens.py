from tokens.ecdsa_token import EcdsaToken
from tokens.rc4_token import RC4Token

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Tokens(metaclass=Singleton):
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


def main():
    t = Tokens()
    s1, s2 =  t.generate_token(b'hui', 'EC256'), t.generate_token(b'hui', 'HMAC128')
    assert t.validate_token(s1)
    assert t.validate_token(s2)
    try:
        t.validate_token(s1[:-1])
        raise "Ti eblan?"
    except:
        pass

if __name__ == "__main__":
    main()
