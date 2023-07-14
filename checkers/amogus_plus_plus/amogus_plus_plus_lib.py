import re
import requests
from bs4 import BeautifulSoup
from checklib import *

PORT = 1984


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def _get_workspace_id(self, href: str) -> str:
        workspace_id = re.search(r'/workspace/(?P<id>[a-z0-9]+)$', href)
        assert workspace_id is not None
        return workspace_id.group('id')

    def register(self, session: requests.Session, username: str, email: str, password: str):
        session.post(
            f'{self.url}/auth/signup',
            data={'username': username, 'email': email, 'password': password},
        )
        token = session.cookies["pb_auth"]
        session.headers["Cookie"] = f"pb_auth={token}"
        self.c.assert_in("pb_auth", session.cookies.keys(), "Unable to sign up")

    def login(self, session: requests.Session, username: str, password: str):
        session.post(
            f'{self.url}/auth/login',
            data={'username': username, 'password': password},
        )
        token = session.cookies["pb_auth"]
        session.headers["Cookie"] = f"pb_auth={token}"
        self.c.assert_in("pb_auth", session.cookies.keys(), "Unable to sign up")

    def logout(self, session: requests.Session):
        session.cookies.clear()
        session.headers.pop('Cookie')

    def create_workspace(
        self, session: requests.Session, name: str, description: str | None
    ) -> str:
        response = session.post(
            f'{self.url}/playground?/createWorkspace',
            data={'name': name, 'description': description},
        )
        try:
            redirect_location = response.json()["location"]
            return self._get_workspace_id(redirect_location)
        except (requests.exceptions.JSONDecodeError, KeyError, AssertionError) as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to create workspace', str(ex))

    def list_workspaces(self, session: requests.Session) -> set[str]:
        response = session.get(f'{self.url}/playground')
        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.find('main')
        workspaces_list = main.find('ul')
        workspaces = map(
            lambda x: self._get_workspace_id(x.attrs['href']), workspaces_list.find_all('a')
        )
        return set(workspaces)

    def get_workspace_description(self, session: requests.Session, id: str) -> str | None:
        response = session.get(f'{self.url}/playground')
        soup = BeautifulSoup(response.text, 'html.parser')
        workspace_anchor = soup.find('a', {'href': f"/workspace/{id}"})
        self.c.assert_neq(workspace_anchor, None, "Unable to get workspace description")
        return workspace_anchor.attrs.get("title")

    def delete_workspace(self, session: requests.Session, id: str):
        response = session.post(
            f'{self.url}/playground?/deleteWorkspace',
            data={'id': id},
        )
        try:
            response_status = response.json()["status"]
            self.c.assert_eq(response_status, 302, "Unable to delete workspace")
        except (requests.exceptions.JSONDecodeError, KeyError) as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to create workspace', str(ex))

    def list_workspace_files(self, session: requests.Session, workspace_id: str) -> set[str]:
        response = session.get(
            f'{self.url}/workspace/{workspace_id}',
        )
        soup = BeautifulSoup(response.content.decode(), 'html.parser')
        try:
            file_divs = soup.find_all('div', {'class': 'file'})
            filenames = set(map(lambda x: x.find('a').string, file_divs))
            return filenames
        except AttributeError as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to retrieve list of files from workspace', str(ex))

    def save_file_to_workspace(
        self, session: requests.Session, workspace_id: str, filename: str, content: str
    ):
        response = session.put(
            f'{self.url}/workspace/{workspace_id}/{filename}',
            json={
                'filename': filename,
                'content': content,
            },
        )
        try:
            ok = response.json()['ok']
            self.c.assert_eq(ok, True, "Unable to save file in workspace")
        except (requests.exceptions.JSONDecodeError, KeyError) as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to save file in workspace', str(ex))

    def get_file_from_workspace(
        self, session: requests.Session, workspace_id: str, filename: str
    ) -> str:
        response = session.get(f'{self.url}/workspace/{workspace_id}/{filename}')
        try:
            return response.json()
        except (requests.exceptions.JSONDecodeError, KeyError) as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to save file in workspace', str(ex))

    def delete_file_from_workspace(
        self, session: requests.Session, workspace_id: str, filename: str
    ):
        response = session.post(
            f'{self.url}/workspace/{workspace_id}?/deleteFile',
            data={'filename': filename},
        )
        try:
            response_type = response.json()["type"]
            self.c.assert_neq(response_type, "error", "Unable to delete file from workspace")
        except (requests.exceptions.JSONDecodeError, KeyError) as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to delete file from workspace', str(ex))

    def execute_file_from_workspace(
        self, session: requests.Session, workspace_id: str, filename: str, stdin: str
    ) -> tuple[set[str], str]:
        response = session.post(
            f'{self.url}/workspace/{workspace_id}/{filename}',
            json={
                'filename': filename,
                'stdin': stdin,
            },
        )
        try:
            json = response.json()
            files = json['files']
            stdout = json['stdout']
            error_msg = json['errorMsg']
            if "Reached iteration limit" in error_msg:
                self.c.cquit(Status.MUMBLE, "Iteration limit too low", "Iteration limit too low")
            self.c.assert_eq(error_msg, '', "Unable to execute script")
            return (set(files), stdout)
        except (requests.exceptions.JSONDecodeError, KeyError) as ex:
            self.c.cquit(Status.MUMBLE, 'Unable to execute script', str(ex))
