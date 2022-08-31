from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
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


class Register(Resource):
    def post(self):
        if request.method == "POST":
            dataGet = request.get_json()
            email = dataGet['email']
            passw = dataGet['password']
            checkuser = User.query.filter_by(email=email).first()
            if checkuser:
                respons ={
                    'message':'Error, this user is already exist',
                    "Status Code": 400
                }
                return jsonify(respons)
            else:
                user = User(email=email, passw=passw)
                db.session.add(user)
                db.session.commit()
                respons = {
                    'message': 'Success',
                    "Status Code": 200
                }
                return jsonify(respons)

class Login(Resource):
    def post(self):
        dataGet = request.get_json()
        email = dataGet['email']
        passw = dataGet['password']
        login = User.query.filter_by(email=email).first()
        if login and login.verify_password(passw):
            respons = {
                'message': 'Success',
                    "Status Code": 200
            }
            return jsonify(respons)
        else:
            respons = {
                'message': 'Error, this user is already exist',
                "Status Code": 400
            }
            return jsonify(respons)

class Delete(Resource):
    def delete(self):
        dataGet = request.get_json()
        email = dataGet['email']
        passw = dataGet['password']
        checkuser = User.query.filter_by(email=email).first()
        if checkuser and checkuser.verify_password(passw):
            db.session.delete(checkuser)
            db.session.commit()
            respons = {
                'message': 'Success',
                "Status Code": 200
            }
            return jsonify(respons)
        else:
            respons = {
                'message': 'Error, this user is already exist',
                "Status Code": 400
            }
            return jsonify(respons)

api.add_resource(Login,"/login")
api.add_resource(Register,"/register")
api.add_resource(Delete,"/deleteUser")



@app.route('/')
def hello_world():
    retJson = {

    }
    return jsonify(message='Start page')

if __name__ == '__main__':
    app.run()

