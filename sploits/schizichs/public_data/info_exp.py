#!/usr/bin/env python3

import requests as re
from sys import argv

ip = argv[1]
port = 9993
print(re.get(f'http://{ip}:{port}/', headers={
    'Accept': 'application/json'
}).text, flush=True)

