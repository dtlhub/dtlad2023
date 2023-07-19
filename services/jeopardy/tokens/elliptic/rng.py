import os
from Crypto.Util.number import bytes_to_long

class RNG:
    def __init__(self) -> None:
        self.state = bytes_to_long(os.urandom(32))
        self.modulus = 2**128
        self.a = 228
        self.b = 0x837d1c76e0f32b2b6b22

    def __clock(self) -> None:
        self.state = (self.a * self.state + self.b) % self.modulus

    def randless(self, bound: int) -> int:
        self.__clock()
        return self.state % bound
