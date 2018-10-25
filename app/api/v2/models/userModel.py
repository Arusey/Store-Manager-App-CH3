import psycopg2
from flask import jsonify, abort, make_response

from .databaseModel import Db

class AdminModel(Db):
    """initialize an admin object"""
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

        db = Db()
        db.create_tables()
        self.conn = db.create_connection()

    def saveAdmin(self):
        cursor = self.conn.cursor()
        cursor.execute(
        "INSERT INTO users(name, email, password, role) VALUES(%s, %s, %s, %s)"
        ,(self.name, self.email, self.password, self.role,)
        )
        cursor.execute("SELECT id FROM users WHERE role = %s", (self.role,))
        row = cursor.fetchone()
        self.id  = row[0]
        print(self.id)
        self.conn.commit()
        self.conn.close()
