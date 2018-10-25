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
