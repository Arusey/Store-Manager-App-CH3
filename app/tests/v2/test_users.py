from .BaseTest import *

class TestMyUsers(TestAllEndpoints):
    def test_complete_signup(self):
        '''tests for a full signup'''
        response = self.test_client.post("api/v2/auth/adminsignup",
                                         data=self.user_admin_details,
                                         headers={
                                         'content-type': 'application/json'
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "user successfully registered")
        self.assertEqual(response.status_code, 201)
    def test_login_success(self):
        '''test for a successful login'''
        response = self.test_client.post("/app/v2/auth/adminlogin",
                                         data=self.login_admin_credentials,
                                         headers={
                                         'content-type': 'application/json'
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "user successfully logged in")
        self.assertEqual(response.status_code, 200)
