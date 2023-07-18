import requests
from checklib import *

PORT = 5001
class CheckMachine:
    @property 
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.port = PORT 
        self.c = checker

    def register_ecdsa(self, session: requests.Session, username: str, password: str, flag: str):
        data = dict()
        data['username'] = username
        data['password'] = password
        data['flag'] = flag
        data['type'] = 'EC256'
        data['iv'] = ''
        ans = session.post(f"{self.url}/register", data = data)

        return ans

    def register_arc(self, session: requests.Session, username: str, password: str, flag: str, iv: str):
        data = dict()
        data['username'] = username
        data['password'] = password
        data['flag'] = flag
        data['type'] = 'EC256'
        data['iv'] = iv
        ans = session.post(f"{self.url}/register", data = data)

        return ans

    def login(self, session: requests.Session, username: str, password: str):
        data = dict()
        data['username'] = username
        data['password'] = password
        data['type'] = 'EC256'
        data['iv'] = ''
        ans = session.post(f"{self.url}/login", data = data)

        return ans

    def home(self, session: requests.Session, iv = ''):
        return session.get(f"{self.url}/home?iv={iv}")


