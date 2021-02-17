from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from auth import authenticate, identity
from user import UserRgister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #/auth
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRgister, '/register')

if __name__ == '__main__':
    app.run(port=3333, debug=True)
