# src/shared/Authentication
import datetime
import os
from functools import wraps

import jwt
from flask import Response, g, json, request

from ..models.UserModel import UserModel


class Auth():
    """
    Auth Class
    """
    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            encoded = jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            )
            return encoded
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps(
                    {'error': 'error in generating user token',
                     "stacktrace": e.__repr__}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            print(token)
            print(os.getenv('JWT_SECRET_KEY'))
            payload = jwt.decode(
                token, os.getenv('JWT_SECRET_KEY'), 'HS256')
            print(payload)
            print(payload)
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {
                'message': 'token expired, please login again',
                "stacktrace": e1.__repr__}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {
                'message': 'Invalid token, please try again with a new token'}
            return re

    # decorator
    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {'error':
                         'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)
        return decorated_auth
