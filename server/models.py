from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from server.config import bcrypt, db




class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-comments.user', '-comments.post',
                       '-votes.user', '-posts.user', '-votes.post')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    votes = db.relationship('Vote', backref='user')

    #password and authentication
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    # field validations
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Please input your username')
        if User.query.filter_by(username=username).first():
            raise ValueError("username already in use")
        
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        import re
        pattern = r'^[a-z]*.[a-z]*@student.moringaschool.com'
        regex = re.compile(pattern)
        if not regex.fullmatch(email):
            raise ValueError("Use a valid Moringa School email!")

        if not email:
            raise ValueError("Please provide email address")
    
        return email


    @validates('full_name')
    def validate_full_name(self, key, full_name):
        if not full_name:
            raise ValueError("Kindly provide your full name")
        return full_name


    def __repr__(self):
        return f'''User {self.username} {self.email} {self.full_name}'''



class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = ('-post.comments', '-user.comments',
                    '-user.posts', '-user.votes', '-post.user', '-post.votes')

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    update_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationships
    # post=db.relationship('Post', backref='comments')
    # user=db.relationship('User', backref='comments')

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("You cannot post an empty comment")
        if len(content) < 25:
            raise ValueError("Comment must be at least 25 characters")
        return content

    #repl
    def __repr__ (self):
        return f'''Content: {self.content}'''


class Post(db.Model, SerializerMixin):

    __tablename__ = 'posts'
    serialize_rules = ('-comments.post', '-comments.user',
                       '-votes.post', '-votes.user', '-user.posts', '-user.comments', '-user.votes')

    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    resources = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    update_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Table relationship
    comments = db.relationship('Comment', backref='post')
    votes = db.relationship('Vote', backref='post')

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError('Please provide your content')

        if len(content) < 300:
            raise ValueError('content must be atleast 300 character long')

        return content

    @validates('phase')
    def validate_phase(self, key, phase):
        if phase not in range(6):
            raise ValueError('phases range feom 0 to 5')
        return phase

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Please provide a title')

        if len(title) not in range(3, 100):
            raise ValueError('Title should be atleast 3 characters long')

        return title

    def __repr__(self):
        return f'''<Title: {self.title}, Content{self.content}>'''


class Vote(db.Model, SerializerMixin):
    __tablename__ = 'votes'

    serialize_rules = ('-user.votes', '-user.comments', '-user.posts', 
                       '-post.comments', '-post.votes', '-post.user')

    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # user = db.relationship("User", back_populates="votes")
    # post = db.relationship("Post", back_populates="votes")

    

    def __repr__ (self):
        return f'''Vote type: {self.vote_type}'''





# Ref: comments.id > users.id // many-to-one
# Ref: comments.id > posts.id // many-to-one

# Ref: posts.id > users.id //many to one

# Ref: votes.id > users.id //many to o/ne
# Ref: votes.id > posts.id //many to one
