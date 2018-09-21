from flask import Flask
# resource represents something that our api represents
# ex. if our api is concerned w students, a student would be a rosource
# a thing that our api can return a create
# usually mapped into database tables as well
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, Items


app = Flask(__name__)
app.secret_key = 'matt'
# every api deals with a class
api = Api(app)

# initialize jwt object
# creates a new endpoint - /auth
# when we call /auth we send a username and password

jwt = JWT(app, authenticate, identity)


# <string: na me> is how we get data from the browser
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

# debuh will give a nice html page and tell you what went wrong if debug=True

# if we import app.py, then everything will run except
# for everything in if __name__ == '__main__':
if __name__ == '__main__':
    app.run(port=5000, debug=True)
