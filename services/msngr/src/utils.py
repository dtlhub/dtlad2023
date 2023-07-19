from random import choice


def random_bytes(size=120):
    return bytes([choice(list(range(256))) for _ in range(size)])
