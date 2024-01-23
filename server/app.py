from flask import request, jsonify, make_response
from flask_restful import Resource

from config import app, api, db
from server.models import  User, Comment, Post, Vote

class Index(Resource):
    def get(self):
        return {"message": "Welcome to Moringa Api"}
    
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(port=5555, debug=True)