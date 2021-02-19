from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from auth import authenticate, identity
from resources.user import UserRgister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'secret_key'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  #/auth
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRgister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=3333, debug=True)
