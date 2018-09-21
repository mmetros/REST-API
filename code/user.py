import sqlite3
from flask import request
from flask_restful import Resource

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # make the connection to the db
        connection = sqlite3.connect('data.db')
        # now we need to interact with the db
        cursor = connection.cursor()
        # create our query
        # WHERE is our filter
        query = "SELECT * FROM users WHERE username=?"

        # run the query
        # pass with a parameter so that username gets a value
        result = cursor.execute(query, (username,))
        # get first row out of result set
        row  = result.fetchone()
        # row* = row[0], row[1], row[2]
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        # make the connection to the db
        connection = sqlite3.connect('data.db')
        # now we need to interact with the db
        cursor = connection.cursor()
        # create our query
        # WHERE is our filter
        query = "SELECT * FROM users WHERE id=?"

        # run the query
        # pass with a parameter so that username gets a value
        result = cursor.execute(query, (_id,))
        # get first row out of result set
        row  = result.fetchone()
        # *row = row[0], row[1], row[2]
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user



class UserRegister(Resource):
    def post(self):

        data = request.get_json()

        if User.find_by_username(data['username']):
            return {"message": "this username is already taken"}, 400

        print(data)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        # commit saves to the disk
        connection.commit()
        connection.close()
        return {"message": "User Created!"}, 201
