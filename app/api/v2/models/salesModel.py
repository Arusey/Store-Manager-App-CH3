import psycopg2
from flask import make_response, jsonify

from .databaseModel import Db

class ModelSales(Db):
    '''initialize a sale'''

    def __init__(self, userid=None, productid=None):
        # if product and userid:
        self.userid = userid
        self.productid = productid

        self.db = Db()
        self.conn = self.db.create_connection()

    def save(self, userid, id):
        '''record a sale'''
        self.db.create_tables()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sales(userid, productid) VALUES(%s, %s)",
            (self.userid, self.productid),)
        self.conn.commit()
        self.conn.close()

    def get(self):
        db = Db()
        self.conn = db.create_connection()
        db.create_tables()
        cursor = self.conn.cursor()
        mysql = "SELECT * FROM sales"
        cursor.execute(mysql)
        sales = cursor.fetchall()
        totalsales = []
        for sale in sales:
            list_of_keys = list(sale)
            singlesale = {}
            singlesale = list_of_keys[0]
            singlesale = list_of_keys[1]
            singlesale = list_of_keys[2]
            totalsales.append(singlesale)
        self.conn.commit()
        return totalsales
