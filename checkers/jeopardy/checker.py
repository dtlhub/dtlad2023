#!/usr/bin/env python3

import sys
import requests
import re

from checklib import *
from jeopardy_lib import *


class Checker(BaseChecker):
    vulns: int = 1
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
    
    def __check_register_rc4(self):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        flag = rnd_string(10)
        iv = rnd_string(20)
        register_ans = self.mch.register_arc(session, username, password, flag, iv)
        register_status = int(register_ans.status_code)
        self.assert_eq(200, register_status, "Cannot register with ARC228")

        home_status = int(self.mch.home(session, iv).status_code)
        self.assert_eq(200, home_status, "Cannot get home with iv on ARC228")
        
        return session.cookies['token'], iv

    def __check_register_ecdsa(self):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        flag = rnd_string(10)
        register_ans = self.mch.register_arc(session, username, password, flag, '')
        register_status = int(register_ans.status_code)

        self.assert_eq(200, register_status, "Cannot register with ECDSA256")

        home_status = int(self.mch.home(session).status_code)
        self.assert_eq(200, home_status, "Cannot get home with iv on ECDSA256")

        return session.cookies['token']

    def __check_auth_by_cookie(self):
        session = get_initialized_session()
        rc4cookie, iv = self.__check_register_rc4()
        session.cookies.update({"Cookie": rc4cookie})

        status = int(self.mch.home(session, iv).status_code)
        self.assert_eq(200, status, "Cannot get home with old cookie on ARC228")

        session = get_initialized_session()
        ecdsacookie = self.__check_register_ecdsa()
        session.cookies.update({"Cookie": ecdsacookie})
        status = int(self.mch.home(session, iv).status_code)
        self.assert_eq(200, status, "Cannot get home with old cookie on ECDSA")

    def check(self):
        self.__check_auth_by_cookie()
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln:str):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        register_ans = self.mch.register_ecdsa(session, username, password, flag)

        self.cquit(Status.OK, username, f'{username}:{password}')

    def get(self, flag_id: str, flag: str, vuln:str):
        session = get_initialized_session()
        username, password = flag_id.split(':')
        ans = self.mch.login(session, username, password)
        assert_eq(200, int(ans.status_code), Status.CORRUPT)

        home = self.mch.home(session).text
        print(home)

        assert_eq(True, flag in home, "", Status.CORRUPT)
        self.cquit(Status.OK)




if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)

