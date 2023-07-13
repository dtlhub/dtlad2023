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
        response = session.post(url, data={
            "username": username,
            "password": password
        })
        self.c.assert_neq(response.cookies.get("token"), None, "Token not set on registration")
        self.c.assert_neq(response.cookies.get("userID"), None, "user ID not set on registration")
        self.c.assert_in("successfully", response.text, "invalid response on registration")

    def login(self, session: requests.Session, username: str, password: str, status: Status):
        url = f'{self.url}/user/login'
        response = session.post(url, data={
            "username": username,
            "password": password
        })
        self.c.assert_neq(response.cookies.get("token"), None, "Token not set on registration", status)
        self.c.assert_neq(response.cookies.get("userID"), None, "user ID not set on registration", status)
        self.c.assert_in("You have successfully logged in", response.text, "invalid response on registration", status)



    def add_lab(self, session: requests.Session, test_result: float, expected_result: float, lab_name: str, comment: str):
        url = f'{self.url}/labs/new'

        response = session.post(url, json={
            "labName": lab_name,
            "expectedResult": expected_result,
            "testResult": test_result,
            "comment": comment
        },headers={"Accept": "application/json"})

        data = self.c.get_json(response, "Invalid response on adding new lab")
        self.c.assert_eq(type(data), dict, "Invalid response on adding new lab")
        self.c.assert_eq(any(lab['expected'] == expected_result for lab in data['payload']), True, "Invalid response on add lab")
        self.c.assert_eq(any(lab['testResult'] == test_result for lab in data['payload']), True, "Invalid response on add lab")
        self.c.assert_eq(any(lab['comment'] == comment for lab in data['payload']), True, "Invalid response on add lab")
        self.c.assert_eq(data['Authorized'], True, "Can't add a lab")

    def get_lab(self, session: requests.Session, lab_name: str, status: Status) -> str: 
        url = f'{self.url}/labs/show'
        response = session.get(url, params={
            'labname': lab_name
        }, headers={
            'Accept': 'application/json'
        })
        data = self.c.get_json(response, "Invalid response on getting labs", status)
        self.c.assert_eq(type(data), dict, "Invalid response on getting lab", status)
        self.c.assert_eq(any(lab['labName'] == lab_name for lab in data['payload']), True, "Invalid response on getting lab", status)

        return data['payload'][0]['comment']
