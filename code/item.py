import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# instead of init we use get
# saying that this resource can only be accessed via a get request
# Item is our Resource
# define the methods the resource will accept
# in our case it only accepts get and post
class Item(Resource):

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        print(row)
        connection.close()
        if row:
            return {"item": { "name": row[0], "price": row[1]}}
        else:
            None

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        print(result)
        connection.commit()
        connection.close()

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        result = cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection =sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['name'], item['price']))
        connection.commit()
        connection.close()

    # we have to authenticate before we run the get method
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item, 200
        else:
            return {"message": "Item not found"}, 404

        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return item, 200 if item is not None else 404

    def post(self, name):
        # get json payload from request
        # force=True ;you do not need content type header to be JSON
        # silent=True ; does not give an error, just returns none
        # request_data = request.get_json(force=True)
        # request_data = request.get_json(silent=True)

        if self.find_by_name(name):
            return {'message': "An item with name {} already exists".format(name)}, 400
        # tell client that we have created the item and added it to the db
        else:
            data = request.get_json()
            item = {'name': name, 'price': data['price']}
            try:
                self.insert(item)
                return {'message': 'Item added into the Database'}
            except:
                return {'message': 'An error occured while inserting the item'}, 500 #internal server error

    def delete(self, name):
        if self.find_by_name(name):
            self.delete_item(name)
            return {'message': 'Item Deleted'}
        else:
            return {'message': 'Item not Found'}

    def put(self, name):
        parser = reqparse.RequestParser()
        # use this parser to make sure certain data is passed through
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        # get data from the request
        # we use request to get data entered in a field
        data = parser.parse_args()
        item = {'name': name, 'price': data['price']}
        # check if the item is already in the list
        if self.find_by_name(name):
            try:
                self.update(item)
                return {'message': 'Item Updated'}
            except:
                return {'message': 'An error occurred updating this item'}, 500
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if the item is not in the database then we will add it
        # item = {'name': data['name'], 'price': data['price']}
        # items.append(item)
        try:
            self.insert(item)
            return {'message': "The item has been added to the DB"}
        except:
            return {'message': 'An error occurred inserting this item'}, 500
        # if the item is in the database then we will update it



class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items ORDER BY name"

        result = cursor.execute(query)
        rows = cursor.fetchall()

        print('Total Row(s):', result.rowcount)
        if rows:
            for row in rows:
                print(row)
            return {"items": rows}
        else:
            return "No Items Found"
