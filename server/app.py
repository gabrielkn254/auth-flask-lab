from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User, Journal, UserSchema, JournalSchema

app = Flask(__name__)
app.secret_key = b'flaskauthlab2026finallabdeployable'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

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