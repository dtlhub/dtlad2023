#!/usr/bin/env python3

import sys
import requests
from string import printable, ascii_letters, digits
from random import choice

from checklib import *
from amogus_plus_plus_lib import *


FILENAME_ALPHA = ascii_letters + digits + '_-'

# Test all statements from the program
INTEGRAL_TEST = '''
'''.strip()

# Ensure we are able to execute 1000 iterations
ITERATION_TEST = '''
RED HAVE YOU SEEN THIS
WHILE ITS NOT RED VOTE ME
BLOCKUS
	CHAR WHO ARE YOU
	CHAR CAN VOUCH GO AND TELL THEM COME ON
	RED HAVE YOU SEEN THIS
ENDBLOCKUS
'''.strip()


class Checker(BaseChecker):
    vulns: int = 3
    timeout: int = 20
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check_auth(self, session: requests.Session):
        username = rnd_username()
        password = rnd_password()
        email = f'{username}@mail.ru'

        self.mch.register(session, username, email, password)
        self.mch.logout(session)
        self.mch.login(session, username, password)

    def check_workspaces(self, session: requests.Session):
        # Create workspace without description
        empty_workspace_name = rnd_string(20)
        empty_desc_workspace_id = self.mch.create_workspace(session, empty_workspace_name, None)
        empty_description = self.mch.get_workspace_description(session, empty_desc_workspace_id)
        self.assert_eq(empty_description, "", "Wrong workspace description")
        files = self.mch.list_workspace_files(session, empty_desc_workspace_id)
        self.assert_eq(files, {"main.sus"}, "Bad initial workspace files")

        # Delete workspace
        self.mch.delete_workspace(session, empty_desc_workspace_id)
        created_workspaces = self.mch.list_workspaces(session)
        self.assert_eq(len(created_workspaces), 0, "Unexpected result after deleting workspace")

        # Create workspace with description
        workspace_name = rnd_string(20)
        workspace_description = rnd_string(20)
        workspace_id = self.mch.create_workspace(session, workspace_name, workspace_description)
        description = self.mch.get_workspace_description(session, workspace_id)
        self.assert_eq(description, workspace_description, "Wrong workspace description")

        # Create many workspaces
        expected_workspaces = {workspace_id}
        for _ in range(3):
            name = rnd_string(20)
            description = rnd_string(20)
            expected_workspaces.add(self.mch.create_workspace(session, name, workspace_description))
        created_workspaces = self.mch.list_workspaces(session)
        self.assert_eq(created_workspaces, expected_workspaces, "Workspace not found")

    def check_files(self, session: requests.Session):
        workspace_name = rnd_string(20)
        workspace_id = self.mch.create_workspace(session, workspace_name, None)

        filename = f'{rnd_string(8, alphabet=FILENAME_ALPHA)}.txt'

        # Create file
        content = rnd_string(300, alphabet=printable)
        self.mch.save_file_to_workspace(session, workspace_id, filename, content)
        files = self.mch.list_workspace_files(session, workspace_id)
        self.assert_eq(files, {"main.sus", filename}, "Bad initial workspace files")
        recieved_content = self.mch.get_file_from_workspace(session, workspace_id, filename)
        self.assert_eq(recieved_content, content, "File content changed")

        # Append to file
        content += rnd_string(300, alphabet=printable)
        self.mch.save_file_to_workspace(session, workspace_id, filename, content)
        files = self.mch.list_workspace_files(session, workspace_id)
        self.assert_eq(files, {"main.sus", filename}, "Bad initial workspace files")
        recieved_content = self.mch.get_file_from_workspace(session, workspace_id, filename)
        self.assert_eq(recieved_content, content, "File content changed")

        # Delete file
        self.mch.delete_file_from_workspace(session, workspace_id, filename)
        files = self.mch.list_workspace_files(session, workspace_id)
        self.assert_eq(files, {"main.sus"}, "Unexpected result after deleting file")

        # Create many files
        expected_files = {"main.sus"}
        for _ in range(3):
            filename = f'{rnd_string(8, alphabet=FILENAME_ALPHA)}.txt'
            self.mch.save_file_to_workspace(session, workspace_id, filename, "")
            expected_files.add(filename)
        created_files = self.mch.list_workspace_files(session, workspace_id)
        self.assert_eq(created_files, expected_files, "File not found")

    def check_script_integral(self, session: requests.Session):
        workspace_name = rnd_string(20)
        workspace_id = self.mch.create_workspace(session, workspace_name, None)

        input_file = f'{rnd_string(8, alphabet=FILENAME_ALPHA)}.txt'
        input_file_content = rnd_string(300, alphabet=printable)
        self.mch.save_file_to_workspace(session, workspace_id, input_file, input_file_content)

        file_to_delete = f'{rnd_string(8, alphabet=FILENAME_ALPHA)}.tmp'
        self.mch.save_file_to_workspace(session, workspace_id, file_to_delete, '')

    def check_script_iterations(self, session: requests.Session):
        workspace_name = rnd_string(20)
        workspace_id = self.mch.create_workspace(session, workspace_name, None)

        self.mch.save_file_to_workspace(session, workspace_id, 'main.sus', ITERATION_TEST)

        stdin = ''.join(choice(ascii_letters) for _ in range(1000 // 6))
        _, stdout = self.mch.execute_file_from_workspace(session, workspace_id, 'main.sus', stdin)
        self.assert_eq(stdin, stdout, 'Wrong script execution result')

    def check(self):
        session = self.get_initialized_session()
        self.check_auth(session)
        self.check_workspaces(session)
        self.check_files(session)
        self.check_script_integral(session)
        self.check_script_iterations(session)
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        # TODO
        self.cquit(Status.OK)

    def get(self, flag_id: str, flag: str, vuln: str):
        # TODO
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
