from .BaseTest import *

class TestSales(TestAllEndpoints):
    def test_sale_success(self):
        response = self.test_client.post("/api/v2/sales",
                                         data=self.sale,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "product successfully sold")
        self.assertEqual(response.status_code, 201)

    def test_empty_sale_data(self):
        response = self.test_client.post("/api/v2/sales",
                                         data=json.dumps({

                                         }),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "no data available")
        self.assertEqual(response.status_code, 406)
        
    def test_get_all_sales(self):
        response = self.test_client.get("/api/v2/sales",
                                         data=self.sale,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "sale retrieval is successful")
        self.assertEqual(response.status_code, 200)

    # def test_no_sale_made(self):
    #     response = self.test_client.get("/api/v2/sales",
    #                                      data=json.dumps({

    #                                      }),
    #                                      headers={
    #                                          'content-type': 'application/json',
    #                                          'x-access-token': self.token_for_admin
    #                                      })
    #     message = json.loads(response.data)
    #     self.assertEqual(message["Message"], "unfortunately no sale has been made")
    #     self.assertEqual(response.status_code, 404)

    # def test_sales_datatype(self):
    #     response = self.test_client.post("/api/v2/sales",
    #                                      data=json.dumps({
    #                                         "id": "hefojwfjo"
    #                                      }),
    #                                      headers={
    #                                          'content-type': 'application/json',
    #                                          'x-access-token': self.token_for_attendant
    #                                      })
    #     message = json.loads(response.data)
    #     print(response.data)
    #     self.assertEqual(message["Message"], "Ensure you have filled up the correct number of fields")
    #     self.assertEqual(response.status_code, 400)



    


 

    
    

    