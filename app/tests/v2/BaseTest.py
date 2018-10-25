import unittest
import json
from app import create_app
from instance.config import app_config
from app.api.v2.models.databaseModel import Db

class TestAllEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(app_config['testing'])
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.db=Db()
        self.user_admin_details = json.dumps({
            "name": "kevin",
            "email": "kevin@email.com",
            "password": "Kevin@463",
            "role": "admin"
        })
        self.login_admin_credentials = json.dumps({
            "email": "kevin@email.com",
            "password": "Kevin@463"
        })
        admin_sign_up = self.test_client.post("api/v2/auth/adminsignup",
                                                data=self.user_admin_details,
                                                headers={
                                                'content-type': "application/json"
                                                })
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        '''Clear all tables in database'''
        self.db.collapse_tables()
        self.context.pop()
