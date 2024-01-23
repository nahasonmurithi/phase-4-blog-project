from flask import Blueprint, make_response, jsonify, request
from config import Api, Resource, reqparse
from server.models import User, Post, Comment, Vote
from server.config import bcrypt, db

user_bp=Blueprint("user_bp", __name__)
api = Api(user_bp)

parse = reqparse.RequestParser()
parse.add_argument('username', type=str, help='Provide username')
parse.add_argument('email', type=str, help='Provide email')
parse.add_argument('confirm password', type=str, help='Provide password confirmation')
parse.add_argument('password', type=str, help='Provide password')

parse.add_argument('full_name', type=str, help='Provide full name')



class Users(Resource):
    def get(self):
        users_lc=[user.to_dict() for user in User.query.all()]

        return make_response(jsonify(users_lc), 200)
    
    def post(self):
        args = parser.parse_args()

        password=args("password")
        confirm_password=args("password")

        if not password == confirm_password:
            
            return {
                "error": "passwords do not match!"
            }
        
        new_user=User(
            username=args["username"]
            email=args["email"]
            _password_hash=bcrypt.generate_password_hash(password.encode('utf-8'))
        )
        db.session.add(new_user)
        db.session.commit()

        response = make_response(jsonify(new_user.to_dict()), 201)
        return response
    

class UserByID(Resource):
    def get(set, user_id):
        user = User.query.filter_by(id==user_id).first()

        if not user:
            return{"error":"user not found"}, 404
        response = make_response(jsonify(user.to_dict()), 200)
        return response
    
    def patch(self, user_id):
        user = User.query.filter_by(id == user_id).first()

        args  = parser.parse_args()

        for attr in args:
            setattr(user, attr, args.get(attr))
        
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)
    

    def delete(self, user_id):
        user = User.query.filter_by(id == user_id).first()

        user_post = Post.query.filter_by(user_id == user_id).all()
        user_comments = Comment.query.filter_by(user_id == user_id).all()
        user_votes = Post.query.filter_by(user_id == user_id).all()

        Post.query.delete(user_posts)
        Comment.query.delete(user_comments)
        Vote.query.delete(user_votes)

        return{"message": "user account deleted successfully"}, 200
    
api.add_resource(User, "/users")
api.add_resource(UserByID, "/users/<int:id>")

