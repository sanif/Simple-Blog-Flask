import logging.config
from os import environ

from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .config import config as app_config
from .models import bcrypt, db

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

    # migration
    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    # Blueprints
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

    @app.route('/', methods=['GET'])
    def index():
        """
        Blog endpoint
        """
        return 'Server is up and running'

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
