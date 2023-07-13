import requests

from checklib import *
from random import uniform

PORT = 9993

def rnd_float(min: float, max: float) -> float:
    return uniform(min, max)

class CheckMachine:
    @property
    def url(self) -> str:
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def register(self, session: requests.Session, username: str, password: str):
        url = f'{self.url}/user/register'
        response = self.post(url, data={
            "username": username,
            "password": password
        })
        self.c.assert_neq(response.cookies.get("token"), None, "Token not set on registration")
        self.c.assert_neq(response.cookies.get("userID"), None, "user ID not set on registration")
        self.c.assert_in("You have successfully registered", response, "invalid response on registration")

    def login(self, session: requests.Session, username: str, password: str, status: Status):
        url = f'{self.url}/user/login'
        response = self.post(ur, data={
            "username": username,
            "password": password
        })
        self.c.assert_neq(response.cookies.get("token"), None, "Token not set on registration", status)
        self.c.assert_neq(response.cookies.get("userID"), None, "user ID not set on registration", status)
        self.c.assert_in("You have successfully logged in", response, "invalid response on registration", status)



    def add_lab(self, session: requests.Session, test_result: float, expected_result: float, comment: str):
        url = f'{self.url}/labs/new'

        response = session.post(url, json={
            "expectedResult": expected_result,
            "testResult": test_result,
            "comment": comment
        },headers={"Accept": "application/json"})

        data = self.c.get_json(response, "Invalid response on adding new lab")
        self.c.assert_eq(type(data), dict, "Invalid response on adding new lab")
        self.c.assert_in(str(expected_result), data, "Invalid response on add lab")
        self.c.assert_in(str(test_result), data, "Invalid response on add lab")
        self.c.assert_in(comment, data, "Invalid response on add lab")
        self.c.assert_eq(data['Authorized'], True, "Can't add a lab")

    def get_labs(self, session: requests.Session, expected_result: float, comment: str, status: Status) -> str: 
        url = f'{self.url}/labs/show'
        response = session.get(url, headers={'Accept': 'application/json'})
        data = self.c.get_json(response, "Invalid response on getting labs", status)
        self.c.assert_eq(type(data), dict, "Invalid response on get_note", status)
        self.c.assert_in(str(expected_result), data, "Invalid response on get_note", status)
        self.c.assert_in(comment, data, "Invalid response on put_note", status)
        found = False
        foundIndex = 0
        for _ in range (len(data['payload']):
            lab = data['payload'][foundIndex]
            if lab['comment'] == comment && lab['expected'] == expected_result:
                found = True
                break
            foundIndex += 1

        self.c.assert_eq(found, True, "Could not find lab", status)
        return data['payload'][foundIndex]['comment']
