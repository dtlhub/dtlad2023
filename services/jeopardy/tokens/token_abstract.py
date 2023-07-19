from abc import ABC


class Token(ABC):
    def __init__(self, key: bytes) -> None:
        pass

    def generate_token(self, data: bytes) -> str:
        pass

    def validate_token(self, token: str) -> bool:
        pass
