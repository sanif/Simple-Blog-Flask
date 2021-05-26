# /src/views/UserView

import marshmallow
from flask import Blueprint, Response, current_app, g, json, request
from werkzeug.local import LocalProxy

from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth as auth

user_api = Blueprint('users', __name__)
logger = LocalProxy(lambda: current_app.logger)

user_schema = UserSchema()


@user_api.route('', methods=['POST'])
def create():
    """
    Create User Function
    """
    req_data = request.get_json()
    try:
        data = user_schema.load(req_data)
    except marshmallow.ValidationError as error:
        return custom_response(error, 400)
    # if error:
    #     return custom_response(error, 400)

    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_username(data.get('username'))
    req_data
    if user_in_db:
        message = {
            'error': 'User already exist, please supply another username'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user)

    token = auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 201)


@user_api.route('/', methods=['GET'])
@auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, 200)


@user_api.route('/me', methods=['DELETE'])
@auth.auth_required
def delete():
    """
    Delete a user
    """
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 204)


@user_api.route('/me', methods=['GET'])
@auth.auth_required
def get_me():
    """
    Get me
    """
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    try:
        data = user_schema.load(req_data, partial=True)
    except marshmallow.ValidationError as error:
        return custom_response(error, 400)

    if not data.get('username') or not data.get('password'):
        return custom_response(
            {'error': 'you need username and password to sign in'}, 400)

    user = UserModel.get_user_by_username(data.get('username'))

    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)

    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    ser_data = user_schema.dump(user)
    print(ser_data.get('id'))
    token = auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
