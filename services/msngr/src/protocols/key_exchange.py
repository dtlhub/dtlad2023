from hashlib import sha512

p = 144982569249120405618398337189647848066750882291964593436576397601600745085795828906894506756653756422025789016276246047439828103490530417126093310330555936334647616565299429669217676190404287522030320353384847606639969893831949168617787758280324566416099625782081485179961083426665131923795387477876479610271


def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5) + 1, 2):
        if basis[i]:
            basis[i * i :: 2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]


def miller_rabin(n, b):
    basis = generate_basis(b)
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


class KeyExchanger:
    def __init__(self, generator, modulus):
        self.__verify(modulus)
        self.generator = generator

    def __verify(self, modulus):
        if not miller_rabin(modulus, 64):
            self.modulus = p
            return
        self.modulus = modulus

    def shared_key(self, alice_public_key: int, bob_private_key: int):
        return hex(pow(alice_public_key, bob_private_key, self.modulus))[2:]

    def generate_public_key(self, alice_private):
        return pow(self.generator, alice_private, self.modulus)

    def derive_key_to_feistel(self, shared_key):
        return sha512(str(shared_key).encode()).hexdigest()
