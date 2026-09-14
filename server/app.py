from flask import make_response, request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Journal, UserSchema, JournalSchema


# IAM routes
class Signup(Resource):
    pass


class CheckSession(Resource):
    pass


class Login(Resource):
    pass


class Logout(Resource):
    pass


# Resources routes
class Journals(Resource):
    pass

# Configure api routes
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check-session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Journals, '/journals')

if __name__ == '__main__':
    app.run(port=5555, debug=True)