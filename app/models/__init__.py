# app/models/__init__.py

from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase
from safrs.api_methods import search, startswith

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()


class BaseModel(SAFRSBase, db.Model):
    __abstract__ = True
    # Add startswith methods so we can perform lookups from the
    # frontend
    SAFRSBase.search = search
    # Needed because we don't want to implicitly commit when using
    # flask-admin
    SAFRSBase.db_commit = False
