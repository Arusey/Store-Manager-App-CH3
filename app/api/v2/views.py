from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import Config
import jwt
import datetime

from .models.userModel import AdminModel
from .utils import AuthValidate, ProductValidate

def token_required(func):
    '''creates a token'''
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({
                                 "Message": "the access token is missing, Login"}, 401))
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            for user in users:
                if user['email'] == data['email']:
                    current_user = user

        except:

            print(Config.SECRET_KEY)
            return make_response(jsonify({
                "Message": "This token is invalid"
            }, 403))

        return func(current_user, *args, **kwargs)
    return decorated



class AdminSignup(Resource):
    """docstring for AdminSignup."""
    def post(self):
        data = request.get_json()
        AuthValidate.validate_empty_data(self, data)
        AuthValidate.validate_data(self, data)
        AuthValidate.validate_details(self, data)
        name = data["name"]
        email = data["email"]
        password = data["password"]
        role = data["role"]
        user = AdminModel(name, email, password, role)
        user.saveAdmin()
        return make_response(jsonify({
        "Message": "user successfully registered",
        "name": name,
        "email": email,
        "role": role
        }), 201)
class AdminLogin(Resource):
    '''docstring for administrator login'''
    def post(self):
        '''login as user and encode a jwt token'''
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        users = AdminModel.get(self)
        for user in users:
            if email == user["email"] and password == user['password']:
                token = jwt.encode({
                "email": email,
                "password" : password,
                "exp": datetime.datetime.utcnow() + datetime.timedelta
                                                (minutes=5)
                }, Config.SECRET_KEY)
                return make_response(jsonify({
                            "Message": "user successfully logged in",
						     "token": token.decode("UTF-8")}), 200)
            return make_response(jsonify({
                "Message": "Login failed, wrong entries"
            }
            ), 403)
