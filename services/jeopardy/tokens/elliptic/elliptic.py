from __future__ import annotations
from dataclasses import dataclass
from tokens.elliptic.rng import RNG
from hashlib import md5
from Crypto.Util.number import long_to_bytes, bytes_to_long

@dataclass
class EllipticCurve:
    p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
    b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

class EllipticPoint:
    def __init__(self, x: int, y: int, curve: EllipticCurve) -> None:
        self.x = x % curve.p
        self.y = y % curve.p
        self.curve = curve

    def __eq__(self, other: 'EllipticPoint') -> bool:
        return self.x == other.x and self.y == other.y

    def __neq__(self, other: 'EllipticPoint') -> bool:
        return not self == other

    def __add__(self, other: 'EllipticPoint') -> EllipticPoint:
        if self.x == 0 and self.y == 0:
            return other
        if other.x == 0 and other.y == 0:
            return self

        if self.x == other.x and self.y == (-other.y) % self.curve.p:
            return EllipticPoint(0, 0, self.curve)

        if self != other:
            lmd = (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)
        else:
            lmd = (3 * (self.x ** 2) + self.curve.a) * pow(self.y * 2, -1, self.curve.p)

        x = ((lmd ** 2) - self.x - other.x) % self.curve.p
        y = (lmd * (self.x - x) - self.y) % self.curve.p

        return EllipticPoint(x, y, self.curve)

    def __mul__(self, other: int) -> EllipticPoint:
        Q = EllipticPoint(self.x, self.y, self.curve)
        R = EllipticPoint(0, 0, self.curve)

        while other != 0:
            if other % 2 == 1:
                R = R + Q
            Q = Q + Q
            other //= 2
        return R

    def __str__(self) -> str:
        return str(self.x)


class ECDSA:
    def __init__(self, key: bytes = b'huijopa'):
        self.curve = EllipticCurve()
        self.G = EllipticPoint(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                               0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
                               self.curve)
        self.d = 1337
        self.Q = self.G * self.d
        self.rng = RNG()

    def sign(self, m: int) -> (int, int):
        m = bytes_to_long(md5(long_to_bytes(m)).digest())
        k = self.rng.randless(self.curve.n - 1)
        r = (self.G * k).x
        if r == 0:
            return self.sign(m)

        s = pow(k, -1, self.curve.n) * (m + self.d * r)
        s %= self.curve.n

        if s == 0:
            return self.sign(m)

        return (r, s)

    def validate(self, m, r, s) -> bool:
        if not 0 < r < self.curve.n:
            return False

        if not 0 < s < self.curve.n:
            return False

        m = bytes_to_long(md5(long_to_bytes(m)).digest())
        w = pow(s, -1, self.curve.n)
        u1 = (m * w) % self.curve.n
        u2 = (r * w) % self.curve.n
        X = self.G * u1 + self.Q * u2
        v = X.x % self.curve.n

        return v == r

def main():
    ecdsa = ECDSA()
    r,s = ecdsa.sign(5)


if __name__ == "__main__":
    main()
