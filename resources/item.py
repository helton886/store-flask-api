from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="You need to inform the price")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="You need to inform the store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'error': 'item not found'}, 404

    @jwt_required()
    def post(self, name):
        item_exists = ItemModel.find_by_name(name)
        if item_exists:
            return {'error': f'an item with {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"error": "Couldn't insert the item into database"}, 500

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)
            if item is None:
                item = ItemModel(name, **data)
            else:
                item.price = data['price']
                item.store_id = data['store_id']
            item.save_to_db()
        except:
            return {"error": "An error occurred while updating the item"}, 500
        return item.json()

    @jwt_required()
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
                return {'message': 'Item deleted'}
        except:
            return {'error': 'An error occurred while deleting the item'}, 500


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
