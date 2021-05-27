import logging.config
from os import environ

import bcrypt
from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_restful import Api, Resource
from safrs import SAFRSAPI, SAFRSBase

from app.models import bcrypt, db, ma
from app.models.PostModel import PostModel
from app.models.UserModel import UserModel

from .config import config as app_config

celery = Celery(__name__)


def create_app():
    """
    Create app
    """
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()

    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)

    # app initializations
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    celery.config_from_object(app.config, force=True)
    # celery is not able to pick result_backend and hence using
    # update
    celery.conf.update(
        result_backend=app.config['RESULT_BACKEND'])

    # Other initializations
    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    # migration
    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    # Blueprints
    create_blueprints(app)

    # Admin
    create_admin(app)

    @app.route('/', methods=['GET'])
    def index():
        """
        Blog endpoint
        """
        return 'Server is up and running'

    with app.app_context():
        # Open APi
        create_api(app)
    return app


def create_blueprints(app):
    from .views.CoreView import core as core_blueprint
    app.register_blueprint(
        core_blueprint,
        url_prefix='/api/v1/core'
    )

    from .views.UserView import user_api as user_blueprint
    app.register_blueprint(
        user_blueprint,
        url_prefix='/api/v1/users'
    )


def create_api(app, HOST="localhost", PORT=5000,
               API_PREFIX="/api/v2"):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(UserModel)
    api.expose_object(PostModel)


def create_admin(app):
    admin = Admin(app, name='Dashboard')
    admin.add_view(ModelView(UserModel, db.session))
    admin.add_view(ModelView(PostModel, db.session))


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
