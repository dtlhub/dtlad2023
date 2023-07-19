#!/usr/bin/env python3

import os
import sys
from string import ascii_letters, digits
from random import choice
from checklib import *  # noqa: F403
from Crypto.Util.number import getPrime

argv = [c for c in sys.argv]  # https://docs.pwntools.com/en/stable/args.html :)))))))))))
os.environ['PWNLIB_NOTERM'] = '1'  # https://stackoverflow.com/a/67183309/15078906 :)))))))))))
from pwn import remote, PwnlibException, context  # IIbIBEH TY/lC b/|RTb  # noqa: E402
from msngr_lib import CheckMachine  # noqa: E402

context.log_level = 'critical'  # bIbIbIbIbIbIbIbIbIbIbI


PORT = 8441


def get_random_hello_string(length:int = 15) -> str:
    alphabet = ascii_letters + digits + r'!#$%&()*+,-./:;<=>?@[]^_`{|}~'
    return ''.join(choice(alphabet) for _ in range(length))


def get_random_secret_string(length: int = 15) -> str:
    alphabet = ascii_letters + digits
    return ''.join(choice(alphabet) for _ in range(length))


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 30
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except PwnlibException as ex:
            self.cquit(Status.DOWN, 'Connection error', f'Got pwntools error: {ex}')

    def get_initialized_session(self) -> remote:
        r = remote(self.host, PORT)
        r.settimeout(5)

        # This hack works, because `pwn.remote` also has method `.close()`
        self._sessions.append(r)  # type: ignore
        # Skip 'welcom to mesfnasensgetR! on SANbKA!!'
        r.recvline()

        return r

    def check_auth(self):
        r1 = self.get_initialized_session()
        username = rnd_username()
        hello_message = get_random_hello_string()
        secret_message = get_random_secret_string()
        token = self.mch.register(r1, username, hello_message, secret_message)

        r2 = self.get_initialized_session()
        self.mch.login(r2, username, token)

        hello_message_stored = self.mch.get_hello_message(r2)
        self.assert_eq(hello_message_stored, hello_message, "Hello message differs")
        secret_message_stored = self.mch.get_secret_message(r2)
        self.assert_eq(secret_message_stored, secret_message, "Secret message differs")

        expected_registered_users = {username}
        for _ in range(4):
            username = rnd_username()
            hello_message = get_random_hello_string()
            secret_message = get_random_secret_string()
            self.mch.register(r2, username, hello_message, secret_message)
            expected_registered_users.add(username)
        registered_users = self.mch.list_users(r1)

        for username in expected_registered_users:
            self.assert_in(username, registered_users, "List of registered users is wrong")

    def check_crypto(self):
        r = self.get_initialized_session()
        username = rnd_username()
        hello_message = get_random_hello_string()
        secret_message = get_random_secret_string()
        self.mch.register(r, username, hello_message, secret_message)

        gen = 2
        mod = getPrime(1024)
        self.mch.init_key_exchange(r, gen, mod)

        ciphertext, key = self.mch.communicate_dh_feistel(r, username)
        decrypted_hello_hex = self.mch.decrypt(r, ciphertext, key)
        decrypted_hello = bytes.fromhex(decrypted_hello_hex)
        self.assert_eq(decrypted_hello, hello_message.encode(), "Decrypt(encrypt(hello)) != hello")

        # TODO: check commuticate_ask_to_encrypt
        # TODO: check communicate_ask_for_secret

    def check(self):
        self.check_auth()
        self.check_crypto()
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        r = self.get_initialized_session()
        username = rnd_username()
        hello_message = get_random_hello_string()
        secret_message = flag
        token = self.mch.register(r, username, hello_message, secret_message)
        self.cquit(Status.OK, username, f"{username}:{token}")

    def get(self, flag_id: str, flag: str, vuln: str):
        username, token = flag_id.split(':')
        r = self.get_initialized_session()
        self.mch.login(r, username, token)
        secret_message = self.mch.get_secret_message(r)
        self.assert_eq(secret_message, flag, "Secret message changed", Status.CORRUPT)
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(argv[2])

    try:
        c.action(argv[1], *argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
