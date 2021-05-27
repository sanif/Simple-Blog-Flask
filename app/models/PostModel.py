# src/models/PostModel.py
import datetime

from slugify import slugify

from . import BaseModel, bcrypt, db, ma


class PostModel(BaseModel):
    """
    Post Model
    """

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    slug = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.title = data.get('title')
        self.slug = slugify(data.get('title'))
        self.contents = data.get('contents')
        self.owner_id = data.get('owner_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return PostModel.query.all()

    @staticmethod
    def get_one_post(id):
        return PostModel.query.get(id)

    @staticmethod
    def get_one_post_by_slug(id):
        return PostModel.query.filter_by(slug=id).first()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class PostSchema(ma.SQLAlchemySchema):
    """
    Post Schema
    """
    class Meta:
        model = PostModel
    id = ma.auto_field()
    title = ma.auto_field()
    slug = ma.auto_field()
    contents = ma.auto_field()
    owner_id = ma.auto_field()
    created_at = ma.auto_field()
    modified_at = ma.auto_field()
