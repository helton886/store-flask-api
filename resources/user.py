import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRgister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="You need to inform your username")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="You need to inform your password")

    def post(self):
        data = UserRgister.parser.parse_args()

        user_exists = UserModel.find_by_username(data['username'])
        if user_exists:
            return {'error': 'user already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created sucessfully."}, 201
