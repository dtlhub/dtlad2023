#!/usr/bin/env python3

import sys
import requests
from string import printable, ascii_letters, digits
from random import choice

from checklib import *
from amogus_plus_plus_lib import *


def generate_var_name() -> str:
    return choice(ascii_letters + '_') + rnd_string(12, alphabet=ascii_letters + digits + '_')


def generate_file_name(ext='.txt') -> str:
    filename = rnd_string(12, alphabet=ascii_letters + digits + '_.-')
    while '..' in filename:
        filename = filename.replace('..', '.')
    return filename.strip('.') + ext


# Test all statements from the program
INTEGRAL_TEST = '''
GAME {file_to_delete} HAS FINISHED

GUYS I CAN VOUCH {var_a} IS 2
GUYS I CAN VOUCH {var_b} IS 5
GUYS I CAN VOUCH {var_c} IS 10

WHILE ITS NOT {var_b} VOTE ME
BLOCKUS
	{var_e} IS JUST LIKE {var_a}
	WHILE ITS NOT {var_e} VOTE ME
	BLOCKUS
		IDK WHAT {var_d} IS BUT ITS BETWEEN 48 AND 57
		{var_d} CAN VOUCH GO AND TELL THEM COME ON
		{var_e} GOES DOWN
	ENDBLOCKUS

	{var_c} CAN VOUCH GO AND TELL THEM COME ON
		
    GUYS I CAN VOUCH {var_f} IS 2
	WHILE ITS NOT {var_f} VOTE ME
	BLOCKUS
		{var_a} GOES UP
		{var_f} GOES DOWN
		IF ITS NOT {var_b} THEN VOTE ME
			{var_b} GOES DOWN
	ENDBLOCKUS
ENDBLOCKUS

GUYS I CAN VOUCH {var_a} IS 48
IDK WHAT {var_b} IS BUT ITS BETWEEN 0 AND 9
WHILE ITS NOT {var_b} VOTE ME
BLOCKUS
    {var_a} GOES UP
    {var_b} GOES DOWN
ENDBLOCKUS
{var_a} CAN VOUCH GO AND TELL THEM COME ON
{var_c} CAN VOUCH GO AND TELL THEM COME ON

{var_a} HAVE YOU SEEN THIS
WHILE ITS NOT {var_a} VOTE ME
BLOCKUS
    {var_b} WHO ARE YOU
    {var_b} HAS JOINED THE {output_file}
    {var_a} HAVE YOU SEEN THIS
ENDBLOCKUS

IS {input_file} EMPTY {var_c} TELL ME PLS PLS PLS
WHILE ITS NOT {var_c} VOTE ME
BLOCKUS
    {var_d} HAS LEFT THE {input_file}
    {var_d} GOES UP BY 10
    {var_d} GOES DOWN BY 123
    {var_d} GOES UP BY 112
    {var_d} GOES DOWN BY 255
    {var_d} CAN VOUCH GO AND TELL THEM COME ON
    IS {input_file} EMPTY {var_c} TELL ME PLS PLS PLS
ENDBLOCKUS

GUYS I CAN VOUCH {var_e} IS 0
GUYS I CAN VOUCH {var_f} IS 1
WHILE ITS NOT {var_f} VOTE ME
BLOCKUS
    {var_f} GOES UP
    {var_f} GOES DOWN BY 10

    GUYS I CAN VOUCH {var_g} IS 1
    IF ITS NOT {var_f} THEN VOTE ME
    GUYS I CAN VOUCH {var_g} IS 0

    IF ITS NOT {var_g} THEN VOTE ME
    GUYS I CAN VOUCH {var_e} IS 1

    {var_f} GOES UP BY 10
    {var_e} WAS THE IMPOSTOR
ENDBLOCKUS
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

        filename = generate_file_name('.txt')

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
            filename = generate_file_name('.txt')
            self.mch.save_file_to_workspace(session, workspace_id, filename, "")
            expected_files.add(filename)
        created_files = self.mch.list_workspace_files(session, workspace_id)
        self.assert_eq(created_files, expected_files, "File not found")

    def check_script_integral(self, session: requests.Session):
        workspace_name = rnd_string(20)
        workspace_id = self.mch.create_workspace(session, workspace_name, None)

        input_file = generate_file_name('.in')
        input_file_content = rnd_string(10, alphabet=printable)
        self.mch.save_file_to_workspace(session, workspace_id, input_file, input_file_content)

        file_to_delete = generate_file_name('.tmp')
        self.mch.save_file_to_workspace(session, workspace_id, file_to_delete, ':D')

        output_file = generate_file_name('.out')

        args = {f"var_{letter}": generate_var_name() for letter in "abcdefg"}
        args['input_file'] = input_file
        args['output_file'] = output_file
        args['file_to_delete'] = file_to_delete
        script = INTEGRAL_TEST.format(**args)

        stdin = rnd_string(10, ascii_letters)
        self.mch.save_file_to_workspace(session, workspace_id, 'main.sus', script)

        files, stdout = self.mch.execute_file_from_workspace(
            session, workspace_id, 'main.sus', stdin
        )
        self.assert_eq(
            files, {"main.sus", input_file, output_file}, "Wrong script execution result"
        )

        stdout_parts = stdout.split('\n')
        self.assert_eq(len(stdout_parts[0]), 2, "Wrong script execution result")
        self.assert_eq(len(stdout_parts[1]), 4, "Wrong script execution result")
        self.assert_eq(len(stdout_parts[2]), 6, "Wrong script execution result")
        self.assert_eq(
            all(x.isdigit() for x in ''.join(stdout_parts[:3])),
            True,
            "Wrong script execution result",
        )
        self.assert_eq(len(stdout_parts[3]), 1, "Wrong script execution result")
        self.assert_in(stdout_parts[3], digits, "Wrong script execution result")
        self.assert_eq(
            '\n'.join(stdout_parts[4:]), input_file_content, "Wrong script execution result"
        )

        output_file_content = self.mch.get_file_from_workspace(session, workspace_id, output_file)
        self.assert_eq(stdin, output_file_content, "Wrong script execution result")

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
