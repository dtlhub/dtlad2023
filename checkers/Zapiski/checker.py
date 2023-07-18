#!/usr/bin/env python3

import sys
import socket

from checklib import *
from Zapiski_lib import *


class Checker(BaseChecker):
    vulns: int = 1 #probably pwnble but flags in same places
    timeout: int = 5
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except (TimeoutError, ConnectionError):
            self.cquit(Status.DOWN, 'Connection error', 'Got socket connection error')

    def check(self):
        session = self.get_initialized_session()
        username = rnd_string(7)
        note_value = rnd_string(20)

        password = self.mch.register(session, username)
        self.mch.login(session, username, password, Status.MUMBLE, True)
        note_name_full = self.mch.put_note(session, note_value)
        value1 = self.mch.get_note(session, note_name_full)
        self.mch.save(session)
        session.close()
        session = self.get_initialized_session()
        self.mch.login(session, username, password, Status.MUMBLE, False)
        value2 = self.mch.get_note(session, note_name_full)
        self.assert_eq(value1, note_value, "Note value is invalid", Status.CORRUPT)
        self.assert_eq(value2, note_value, "Note not saving", Status.MUMBLE)

        self.cquit(Status.OK)
    
    def get_initialized_session(self) -> socket.socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.mch.port))
        s.settimeout(10)
        return s

    def put(self, flag_id: str, flag: str, vuln: str):
        session = self.get_initialized_session()
        username = rnd_string(7)
        password = self.mch.register(session, username)
        self.mch.login(session,username, password, Status.MUMBLE,True)
        note_id = self.mch.put_note(session, flag)
        self.mch.save(session)
        session.close()
        self.cquit(Status.OK, f'{username}:{note_id}', f'{username}:{password}:{note_id}')

    def get(self, flag_id: str, flag: str, vuln: str):
        session = self.get_initialized_session()
        username, password, note_name_full = flag_id.split(':')
        self.mch.login(session, username, password, Status.MUMBLE, False)
        value = self.mch.get_note(session, note_name_full)
        self.assert_eq(value, flag, "Note value is invalid", Status.CORRUPT)
        session.close()
        self.cquit(Status.OK, f'', f'')


if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
