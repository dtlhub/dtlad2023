import requests as re
from sys import argv
import secrets
import string
import random
from z3 import Real,Solver
from math import *


def rnd_string(length, alphabet=None) -> str:
    if alphabet is None:
        alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


session = re.Session()
ip = argv[1]
port = 9993
url = f"http://{ip}:{port}"

creds = {
    'username': rnd_string(10),
    'password': rnd_string(10)
}


def register():
    session.post(f"{url}/user/register", data=creds)


def postLab(lab_name: str, test_res: float = None, exp_res: float = None, comment: str = ""):
    if test_res is None:
        test_res = random.uniform(100000000, 99999999999)
    if exp_res is None:
        exp_res = random.uniform(0, 123)
    lab_data = {
        'labName': lab_name,
        'testResult': test_res,
        'expectedResult': exp_res,
        'comment': comment
    }
    session.post(f"{url}/lab/new", data=lab_data)


# Here you should parse attack data
def parse_labs():
    return session.get(url, headers={'Accept': 'application/json'}).json()['publicResults']



def sin_as_sum(x,prec):
    return sum(pow(-1,n)/factorial(2 * n + 1)* pow(x,2 * n + 1) for n in range(prec))

def cos_as_sum(x,prec):
    return sum(pow(-1,n)/factorial(2 * n) * pow(x, 2 * n) for n in range(prec))

def tg_as_sum(x,prec):
    return sin_as_sum(x,prec)/cos_as_sum(x,prec)

def solveEq(exp_res: float) -> float:
    x = Real('x')
    s = Solver()
    s.add(x > exp_res + 10000, tg_as_sum(x * 100, 30) < 0.01)
    print(s.check())
    1/0
    x = sp.symbols('x')
    expr = sp.tan(x) < 0.1
    xValue = sp.solve([expr, x > exp_res + 1000000], x, domain=sp.S.Reals)
    print(xValue)



register()
lab_array = parse_labs()

solveEq(123)
