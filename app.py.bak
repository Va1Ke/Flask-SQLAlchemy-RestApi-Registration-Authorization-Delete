from flask import Flask, jsonify, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    passw = db.Column(db.Integer)
    date_joined = db.Column(db.Date, default=datetime.utcnow())

    def __init__(self, email, passw):
        self.passw = generate_password_hash(passw)
        self.email = email

    def verify_password(self, pwd):
        return check_password_hash(self.passw, pwd)

@app.route('/')
def hello_world():
    retJson = {

    }
    return jsonify(message='Start page')

@app.route('/login', methods=['POST'])
def login():
    dataGet = request.get_json()
    email = dataGet['email']
    passw = dataGet['password']
    login = User.query.filter_by(email=email).first()
    if login and login.verify_password(passw):
        return jsonify(message='Success'), 200
    else:
        return jsonify(message='Error, no such user'), 400

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        dataGet = request.get_json()
        email = dataGet['email']
        passw = dataGet['password']
        checkuser = User.query.filter_by(email=email).first()
        if checkuser:
            return jsonify(message='Error, this user is already exist'), 400
        else:
            user = User(email=email, passw=passw)
            db.session.add(user)
            db.session.commit()
            return jsonify(message='Success'), 200

@app.route('/delete_user', methods=['DELETE'])
def deleteUser():
    dataGet = request.get_json()
    email = dataGet['email']
    passw = dataGet['password']
    checkuser = User.query.filter_by(email=email).first()
    if checkuser and checkuser.verify_password(passw):
        db.session.delete(checkuser)
        db.session.commit()
        return jsonify(message='Success'), 200
    else:
        return jsonify(message='Error, no such user'), 400



if __name__ == '__main__':
    app.run()

