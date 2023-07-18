from flask import Flask, make_response, render_template
from flask import request, redirect, url_for
from flask import session
from tokens.tokens import Tokens
from database.database import Database
import json

app = Flask(__name__)
db = Database()
app.secret_key = 'kek'

@app.route('/', methods=['GET'])
def init():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    signature_type = request.form['type']
    flag = request.form['flag']
    password = request.form['password']
    if not db.register(username,password,flag):
        return render_template('register.html', error='User exists')

    try:
        assert len(request.form['iv']) != 0
        token_server = Tokens(bytes.fromhex(request.form['iv']))
    except:
        token_server = Tokens()
    
    to_sign = dict()
    to_sign['username'] = username.encode().hex()
    cookie = token_server.generate_token(json.dumps(to_sign).encode(), signature_type)

    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token', cookie )

    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    signature_type = request.form['type']
    password = request.form['password']

    if not db.login(username, password):
        return render_template('login.html', error='Bad login')

    try:
        assert len(request.form['iv']) != 0
        token_server = Tokens(bytes.fromhex(request.form['iv']))
    except:
        token_server = Tokens()

    to_sign = dict()
    to_sign['username'] = username.encode().hex()
    cookie = token_server.generate_token(json.dumps(to_sign).encode(), signature_type)
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token', cookie )

    return resp


@app.route("/home", methods=['GET'])
def home():
    if 'token' not in request.cookies.keys():
        return redirect(url_for('register'))
    try:
        assert len(request.args['iv']) != 0
        token_server = Tokens(bytes.fromhex(request.args['iv']))
    except Exception as e:
        token_server = Tokens()

    assert token_server.validate_token(request.cookies['token'])

    user = token_server.get_data(request.cookies['token'])['username']
    user = bytes.fromhex(user).decode()

    return render_template('home.html',flag=db.get_flag(user))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True)
