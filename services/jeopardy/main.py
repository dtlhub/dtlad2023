from flask import Flask, make_response, render_template
from flask import request, redirect, url_for
from flask import session
from tokens.tokens import Tokens
from database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def init():
    return render_template('home.html')

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
        token_server = Tokens(bytes.fromhex(request.form['iv']))
    except:
        token_server = Tokens()

    cookie = token_server.generate_token(username.encode(), signature_type)
    session['cookie'] = cookie

    return redirect(url_for('home'))

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
        token_server = Tokens(bytes.fromhex(request.form['iv']))
    except:
        token_server = Tokens()

    cookie = token_server.generate_token(username.encode(), signature_type)
    session['cookie'] = cookie

    return redirect(url_for('home'))


@app.route("/home", methods=['GET'])
def home():
    if 'cookie' not in session.keys():
        return redirect(url_for('register'))

    try:
        token_server = Tokens(bytes.fromhex(request.args['iv']))
    except:
        token_server = Tokens()
    assert token_server.validate_token(session['cookie'])
    #add params for flag in home

    return render_template('home.html', [])
