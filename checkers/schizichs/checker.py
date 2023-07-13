#!/usr/bin/env python3
import sys
import requests

from checklib import *
from schizics_lib import *


class Checker(BaseChecker):
    vulns: int = 3
    timeout: int = 5
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        comment = rnd_string(20)
        lab_name = rnd_string(15)
        expected_result = rnd_float(1, 300)
        test_result = rnd_float(10000003000, 999999999999999)

        self.mch.register(session, username, password)
        self.mch.login(session, username, password, Status.MUMBLE)
        self.mch.add_lab(session, test_result, expected_result, lab_name, comment)
        value = self.mch.get_lab(session, lab_name, Status.MUMBLE)

        self.assert_eq(value, comment, "Lab comment is not valid")
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        lab_name_full = rnd_string(10)
        if vuln == "1":
            lab_name_full += "_1"
        elif vuln == "2":
            lab_name_full += "_2"
        elif vuln == "3":
            lab_name_full += "_3"

        lab_name_public = lab_name_full[:5]

        expected_result = rnd_float(1, 300)
        test_result = rnd_float(10000003000, 999999999999999)

        self.mch.register(session, username, password)
        self.mch.login(session, username, password, Status.MUMBLE)
        self.mch.add_lab(session, test_result, expected_result, lab_name_full, flag)
        self.cquit(Status.OK, lab_name_public, f'{username}:{password}:{lab_name_full}')

    def get(self, flag_id: str, flag: str, vuln: str):
        s = get_initialized_session()
        username, password, note_name_full = flag_id.split(':')

        self.mch.login(s, username, password, Status.CORRUPT)
        value = self.mch.get_lab(s, note_name_full, Status.CORRUPT)

        self.assert_eq(value, flag, "Note value is invalid", Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
