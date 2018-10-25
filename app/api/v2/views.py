from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import app_config
import jwt
import datetime

from .models.userModel import AdminModel

class AdminSignup(Resource):
    """docstring for AdminSignup."""
    def post(self):
        data = request.get_json()
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
