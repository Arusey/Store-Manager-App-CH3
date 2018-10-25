from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import Config
import jwt
import datetime

from .models.userModel import AdminModel
from .models.productModel import ModelProduct
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
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            print(data)
            newuser = AdminModel()
            users = newuser.get()
            for user in users:
                print(users)
                if user['email'] == data['email']:
                    current_user = user
        except Exception as e:
            print(e)
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
                }, Config.SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({
                            "Message": "user successfully logged in",
						     "token": token.decode("UTF-8")}), 200)
            return make_response(jsonify({
                "Message": "Login failed, wrong entries"
            }
            ), 403)


class Product(Resource):
    @token_required
    def post(current_user, self):
        '''endpoint for posting a product'''
        if current_user and current_user["role"] != "admin":
            return make_response(jsonify({
                "Message": "you must be an admin endpoint"}
            ), 403)
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                "Message": "Kindly ensure you have inserted your details"
            }), 400)
        ProductValidate.validate_key_products(self, data)

        name = data["name"]
        category = data["category"]
        description = data["description"]
        currentstock = data["currentstock"]
        minimumstock = data["minimumstock"]
        price = data["price"]

        product = ModelProduct(data)
        product.add_product()
        return make_response(jsonify({
            "Status": "ok",
            "Message": "Product posted successfully",
            "Products": product.get(self)
        }
        ), 201)

    @token_required
    def get(current_user, self):
        '''endpoint for getting all products'''

        if current_user:
            product = ModelProduct()
            products = product.get()
            if len(products) == 0:
                return  make_response(jsonify({
                    "Message": "No products have been posted yet"
                }), 404)
            return make_response(jsonify({
                "Status": "ok",
                "Message": "All products fetched successfully",
                "products": products
            }
            ), 200)
        return make_response(jsonify({
            "Message": "Please login first"
        }), 401)
class SingleProduct(Resource):
    @token_required
    def get(current_user, self, id):
        '''gets single product'''
        product = ModelProduct()
        products = product.get()
        if len(products) == 0:
            return make_response(jsonify({
                "Message": "No products have been posted yet"
            }), 404)
        if current_user:
            for product in products:
                if int(id) == product["id"]:
                    return make_response(jsonify({
                    "Message": "Product retrieval successful",
                    "product": product
                    }), 200)
        return make_response(jsonify({
            "Message": "This product does not exist"
        }), 404)
    @token_required
    def delete(current_user, self, id):
        '''deletes a selected product'''
        product = ModelProduct()
        products = product.get()
        if current_user["role"] != "admin":
            return make_response(jsonify({
                "Message": "You have no authorization to delete a product"
            }), 403)
        for item in products:
            if id == item["id"]:
                product.delete(id)
                message = make_response(jsonify({
                    "message": "Deleted successfully"
                }), 200)
                return message
        message = make_response(jsonify({
            "Message": "The product selected for deletion does not exist"
        }))

        return message
