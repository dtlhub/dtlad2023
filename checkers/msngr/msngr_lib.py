import json
from typing import Tuple, Dict, Any, Set
from string import hexdigits

from checklib import *
from pwn import remote


class ApiException(Exception):
    status: str
    trace: str
    verbose_description: str

    def __init__(self, status, trace, verbose_description):
        self.status = status
        self.trace = trace
        self.verbose_description = verbose_description


class CheckMachine:
    def __init__(self, checker: BaseChecker):
        self.c = checker

    def _send_object(self, io: remote, obj: Dict[str, Any]):
        before_send = json.dumps(obj).encode()
        io.sendline(before_send)

    def _try_get_from_json(self, line: bytes, field: str, type: type, err_msg: str):
        try:
            value = json.loads(line.decode())[field]
            assert isinstance(value, type)
            return value
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, AssertionError):
            self.c.cquit(Status.MUMBLE, err_msg, f"Failed to get field {field} on object {line}")

    def login(self, io: remote, username: str, token: str):
        before_send = json.dumps({"option": "login", "login": username, "token": token}).encode()
        io.sendline(before_send)
        return self._try_get_from_json(io.recvline(), "message", str, "Failed to log in")  # type: ignore

    def register(self, io: remote, username: str, hello_message: str, secret_message: str) -> str:
        self._send_object(
            io,
            {
                "option": "register",
                "login": username,
                "hello_message": hello_message,
                "secret_message": secret_message,
            },
        )
        return self._try_get_from_json(io.recvline(), "token", str, "Failed to register")  # type: ignore

    def get_hello_message(self, io: remote) -> str:
        self._send_object(io, {"option": "get_hello_message"})
        return self._try_get_from_json(io.recvline(), "message", str, "Failed to get hello message")  # type: ignore

    def get_secret_message(self, io: remote) -> str:
        self._send_object(io, {"option": "get_secret_message"})
        return self._try_get_from_json(io.recvline(), "message", str, "Failed to get secret message")  # type: ignore

    def list_users(self, io: remote) -> Set[str]:
        self._send_object(io, {"option": "list_users"})
        users: list = self._try_get_from_json(
            io.recvline(), "users", list, "Failed to get users"
        )  # type: ignore
        self.c.assert_eq(all(isinstance(user, str) for user in users), True, "Failed to get users")
        return set(users)

    def init_key_exchange(self, io: remote, generator: int, modulus: int) -> str:
        self._send_object(
            io,
            {
                "option": "init_key_exchange",
                "generator": hex(generator)[2:],
                "modulus": hex(modulus)[2:],
            },
        )
        return self._try_get_from_json(io.recvline(), "message", str, "Failed to init key exchange")  # type: ignore

    def communicate_dh_feistel(self, io: remote, friend: str) -> Tuple[str, str]:
        self._send_object(io, {"option": "communicate_dh_feistel", "friend": friend})
        response = io.recvline()
        message: str = self._try_get_from_json(
            response, "message", str, "Failed to communicate via dh_feistel"
        )  # type: ignore
        cipher_key: str = self._try_get_from_json(
            response, "message", str, "Failed to communicate via dh_feistel"
        )  # type: ignore
        return message, cipher_key

    def communicate_ask_to_encrypt(self, io: remote, data: str, friend: str) -> str:
        self._send_object(
            io, {"option": "communicate_ask_to_encrypt", "data": data, "friend": friend}
        )
        return self._try_get_from_json(io.recvline(), "message", str, "Failed to ask to encrypt")  # type: ignore

    def communicate_ask_for_secret(self, io: remote, friend: str):
        self._send_object(io, {"option": "communicate_ask_for_secret", "friend": friend})
        return self._try_get_from_json(io.recvline(), "message", str, "Failed to ask to secret")  # type: ignore

    def decrypt(self, io: remote, ct: str, key: str) -> str:
        self._send_object(io, {"option": "decrypt", "ciphertext": ct, "key": key})
        response: str = self._try_get_from_json(io.recvline(), "message", str, "Failed to decrypt")  # type: ignore
        self.c.assert_eq(
            all(char in hexdigits for char in response),
            True,
            "Got non-hex result from description",
        )
        return response
