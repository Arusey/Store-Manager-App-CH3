import unittest
import json


from instance.config import Config
from app import create_app
from app.api.v2.models.databaseModel import Db
from app.api.v2.models import userModel

class TestAllEndpoints(unittest.TestCase):
    '''setup methods to post product, sales and create users'''

    def setUp(self):
        self.db = Db()
        self.db.create_tables()
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.administrator = json.dumps({
            "name": "mercy",
            "email": "mercy@email.com",
            "password": "Mercy@123",
            "role": "admin"
        })
        self.admin_login = json.dumps({
            "email": "mercy@email.com",
            "password": "Mercy@123"
        })
        admin = self.test_client.post("/api/v2/auth/adminsignup",
                                        data=self.administrator,
                                        headers={
                                            'content-type': 'application/json'
                                        })
        login_admin = self.test_client.post("/api/v2/auth/adminlogin",
                                            data=self.admin_login,
                                            headers={
                                                'content-type': 'application/json'
                                            })

        print(json.loads(admin.data.decode()))
        # self.token_for_admin = json.loads(login_admin.data.decode())
        self.data = json.loads(login_admin.data.decode())
        self.token_for_admin = self.data["token"]


        self.attendant = json.dumps({
            "name": "faith",
            "email": "faith@email.com",
            "password": "Faith@123",
            "role": "attendant"
        })
        self.attendant_login = json.dumps({
            "email": "faith@email.com",
            "password": "Faith@123"
        })
        signup_attendant = self.test_client.post("/api/v2/auth/attsignup",
                                                    data=self.attendant,
                                                    headers={
                                                        'content-type': 'application/json',
                                                        'x-access-token': self.token_for_admin})
        login_attendant = self.test_client.post("/api/v2/auth/login",
                                                data=self.attendant_login,
                                                headers={
                                                    'content-type': 'application/json'})
        self.data = json.loads(login_attendant.data.decode())
        print(json.loads(login_attendant.data.decode()))
        self.token_for_attendant = self.data["token"]
        # self.token_for_attendant = json.loads(login_attendant.data.decode())


        self.product = json.dumps(
            {
                "name": "chai",
                "category": "food",
                "description": "Great food",
                "currentstock": 20,
                "minimumstock": 2,
                "price": 200
            }
        )
        self.soldout = json.dumps({
            "name": "chai",
            "category": "food",
            "description": "Great food",
            "currentstock": 0,
            "minimumstock": 0,
            "price": 200
        })
        self.sale = json.dumps ({
            "id": 1
        })
        self.test_client.post("/api/v2/products", data=self.product,
                                headers={
                                    'content-type': 'application/json',
                                    'x-access-token': self.token_for_admin
                                })
        self.test_client.post("/api/v2/sales", data=self.sale,
                                headers={
                                'content-type': 'application/json',
                                'x-access-token': self.token_for_attendant
                                })
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        '''clear all tables and data prior to next test'''
        self.db.collapse_tables()
        self.context.pop()
