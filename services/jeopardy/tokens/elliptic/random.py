import os 
from Crypto.Util.number import bytes_to_long

class RNG:
    def __init__(self) -> None:
        self.state = bytes_to_long(os.urandom(32))
        self.modulus = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        self.a = -1
        self.b = 0x837d1c76e0f32b2b6b226e0135c5f88069768bd796893c15761e66a352abfbb8

    def __clock(self) -> None:
        self.state = self.a * self.state + self.b

    def randless(self, bound: int) -> int:
        self.__clock()
        return self.state % bound
