# src/models/UserModel.py
import datetime

from flask_restful import Resource
from safrs.base import SAFRSBase

import app.models.PostModel

from . import BaseModel, bcrypt, db, ma


class UserModel(BaseModel):
    """
    User Model
    """

    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    posts = db.relationship('PostModel', backref='users', lazy=True)
    # http_methods = {"GET", "POST"}
    # class constructor

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':  # add this new line
                self.password = self.__generate_hash(
                    item)  # add this new line
        setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(
            password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_username(username):
        return UserModel.query.filter_by(username=username).first()

    def __repr(self):
        return '<username {}>'.format(self.username)


class UserSchema(ma.SQLAlchemySchema):
    """
    User Schema
    """
    class Meta:
        model = UserModel
    id = ma.auto_field()
    name = ma.auto_field()
    username = ma.auto_field()
    created_at = ma.auto_field()
    modified_at = ma.auto_field()
    posts = ma.auto_field()
