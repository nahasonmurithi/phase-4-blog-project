from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
   
 
    def __repr__ (self):
        return f'''User{self.username}, Email{self.email}'''



class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    update_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__ (self):
        return f'''Content: {self.content}'''


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'


    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.Integer)
    preview = db.Column(db.String, nullable=False)
    minutes_to_read = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    resources = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    update_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__ (self):
        return f'''Title: {self.title}, Content{self.content}'''

class Vote(db.Model, SerializerMixin):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.Boolean)
    user_id = db.Column(db.Integer. db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    

    def __repr__ (self):
        return f'''Vote type: {self.vote_type}'''





Ref: comments.id > users.id // many-to-one
Ref: comments.id > posts.id // many-to-one

Ref: posts.id > users.id //many to one

Ref: votes.id > users.id //many to one
Ref: votes.id > posts.id //many to one
