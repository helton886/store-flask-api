from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from auth import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #/auth
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="You need to inform the price")
    data = parser.parse_args()

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            return {'item': item}
        return {'error': 'item no found'}, 404

    def post(self, name):
        if next(filter(lambda item: item["name"] == name, items),
                None) is not None:
            return {'error': f'an item with {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=3333, debug=True)
