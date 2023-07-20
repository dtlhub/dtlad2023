from db import Database
from utils import random_bytes
from protocols.key_exchange import KeyExchanger
from protocols.cipher import Cipher


class Messanger:
    def __init__(self):
        self.database = Database()

    def login(self, login, token):
        user_data = self.database.get_user_info(login)
        if len(user_data) == 0:
            return {"error": "User with this login doesn`t exist"}
        if token != user_data[1]:
            return {"error": "Incorrect token"}
        self.username = user_data[0]
        self.secret_key = user_data[1]
        self.hello_message = user_data[2]
        self.secret_message = user_data[3]
        return {"message": "Success"}

    def get_hello_message(self):
        if not self.is_loggined():
            return {"error": "You must login first"}
        return {"message": self.hello_message}

    def get_secret_message(self):
        if not self.is_loggined():
            return {"message": "You must login first"}
        return {"message": self.secret_message}

    def register(self, login, hello_message, secret_message):
        token = random_bytes().hex()
        ans, status = self.database.add_user(login, token, hello_message, secret_message)
        if status:
            response = {"message": ans, "token": token}
            self.username = login
            self.secret_key = token
            self.hello_message = hello_message
            self.secret_message = secret_message
        else:
            response = {"error": ans}
        return response

    def list_users(self):
        return {"users": self.database.users_list()}

    def init_key_exchange(self, generator, modulus):
        self.key_exchange = KeyExchanger(int(generator, 16), int(modulus, 16))
        return {"message": "Success"}

    def has_key_exchanger(self):
        return hasattr(self, 'key_exchange')

    def is_loggined(self):
        return hasattr(self, 'username')

    def communicate_dh_feistel(self, other_username):
        if not self.is_loggined():
            return {"error": "You must login first"}

        if not self.has_key_exchanger():
            return {"error": "You must specify key exchange first"}

        other_user_data = self.database.get_user_info(other_username)
        if len(other_user_data) == 0:
            return {"error": "User with this login doesn`t exist"}

        alice_public = self.key_exchange.generate_public_key(int(self.secret_key, 16))
        shared_key = self.key_exchange.shared_key(alice_public, int(other_user_data[1], 16))
        feistel_key = self.key_exchange.derive_key_to_feistel(int(shared_key, 16))
        cipher = Cipher(bytes.fromhex(feistel_key))
        encrypted_hello = cipher.encrypt(other_user_data[2].encode()).hex()

        return {"message": encrypted_hello, "cipher_key": feistel_key, "shared_key": shared_key}

    def decrypt(self, ciphertext, key):
        cipher = Cipher(bytes.fromhex(key))
        return {"message": cipher.decrypt(bytes.fromhex(ciphertext)).hex()}

    def communicate_ask_to_encrypt(self, message, other_username):
        other_user_data = self.database.get_user_info(other_username)
        if len(other_user_data) == 0:
            return {"error": "User with this login doesn`t exist"}

        feistel_key = bytes.fromhex(other_user_data[1])
        cipher = Cipher(feistel_key)
        return {"message": cipher.encrypt(bytes.fromhex(message)).hex()}

    def communicate_ask_for_secret(self, other_username):
        other_user_data = self.database.get_user_info(other_username)
        if len(other_user_data) == 0:
            return {"error": "User with this login doesn`t exist"}

        feistel_key = bytes.fromhex(other_user_data[1])
        cipher = Cipher(feistel_key)

        return {"message": cipher.encrypt(other_user_data[3]).hex()}
