import socket,re
from checklib import *

PORT = 5712

class CheckMachine:
    @property
    def addresss(self):
        return f'{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def register(self, conn: socket.socket, username: str) -> str:
        conn.recv(1024)
        conn.send(b'2\n')
        conn.recv(1024)
        conn.send(username.encode() + b'\n')
        conn.recv(1024).decode()
        out = conn.recv(1024).decode()
        password = re.findall(r'.+', out)[0]
        password = re.findall(r'[0-9,A-z]+', password)[0]
        return password

    def login(self, conn: socket.socket, username_1: str, password: str, status: Status, registred: bool) -> str:
        if not registred:
            conn.send(b'1\n')
            conn.recv(1024)
        check = conn.send(password.encode() + b'\n')
        out = conn.recv(1024).decode()
        out += conn.recv(1024).decode()
        print(out)
        username = re.findall(r'[0-9,A-z]+!', out)[0]
        username = username[:-1]
        self.c.assert_eq(username, username_1, 'Can\'t login', status)
        return username

    def put_note(self, conn: socket.socket, note_value: str):   
        conn.send(b'1\n')
        conn.recv(1024)
        conn.send(note_value.encode() + b'\n')
        out = conn.recv(1024).decode()
        note_id = re.findall(r'[0-9]+', out)[0]
        conn.recv(1024)
        return note_id
    
    def save(self, conn: socket.socket):
        conn.send(b'3\n')
        
    def get_note(self, conn: socket.socket, note_id: str) -> str:
        conn.send(b'2\n')
        conn.recv(1024)
        conn.send(note_id.encode() + b'\n')
        out = conn.recv(4096).decode()
        note = re.findall(r'.+', out)
        note = note[0]
        return note
