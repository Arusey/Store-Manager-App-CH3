
from flask import Flask, Blueprint
from flask_restful import Api, Resource
from .views import Product, SingleProduct, Login, Sale, SignUp, SingleSale
'''creates our Blueprint'''
mydbblue = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(mydbblue)
'''includes all our routes and classes'''
api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<int:id>')
api.add_resource(SignUp, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Sale, '/sales')
api.add_resource(SingleSale, '/sales/<int:saleid>')
