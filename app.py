from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdoinas87dsnkajsdhu76asdASNNdasdmnasdn87'

users = {

    "admin": {"username": "admin", "password": "1111", "role": "admin"},
    "user": {"username": "user", "password": "1111", "role": "user"}
}


def get_user(username, password):
    for u in users:
        if u == username and users[u]['password'] == password:
            return users[u]
    return None


@app.route("/login", methods=['POST'])
def login():
    data = request.json

    if not data:
        return jsonify({"result": "error", "message": "no data submitted"})
    elif not data.get('username') or not data.get('password'):
        return jsonify({"result": "error", "message": "username/password missing"})
    else:
        username = data.get('username')
        password = data.get('password')
        user = get_user(username, password)
        if user is None: 
            return jsonify({"result": "error", "message": "wrong credentials"})
        else:
            token = jwt.encode({
                'username': username,
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'])
            return jsonify({"result": "success", "token": token})


def role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            return f(data['role'], *args, **kwargs)
        else:
            return f('guest', *args, **kwargs)
    return decorated



@app.route("/")
def home():
    return jsonify({"result": "success", "content": "Home Page"})

@app.route("/info")
@role_required
def info(role):
    if role == 'user':
        return jsonify({"result": "success", "content": "Info Page"})
    else:
        return jsonify({"result": "error", "message": "no access"})

@app.route("/dashboard")
@role_required
def dashboard(role):
    if role == 'admin':
        return jsonify({"result": "success", "content": "Admin Page"})
    else:
        return jsonify({"result": "error", "message": "no access"})
