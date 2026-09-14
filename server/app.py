from flask import make_response, request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Journal, UserSchema, JournalSchema


# IAM routes
class Signup(Resource):
    def post(self):
        request_json = request.get_json(silent=True)

        username = request_json.get("username").strip()
        password = request_json.get("password").strip()

        if not username:
            return make_response(
                {"message": "Invalid username"}, 400
            )

        user = User(username=username)
        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            return make_response(UserSchema().dump(user), 201)
        except IntegrityError:
            return make_response(
                {"error": "Unprocessable Entity"}, 422
            )


class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return make_response(
                UserSchema().dump(user), 200
                )

        return make_response(
            {"message": "Not logged in"}, 401
            )


class Login(Resource):
    def post(self):
        request_json = request.get_json(silent=True)
        
        username = request_json.get("username").strip()
        password = request_json.get("password").strip()

        if not username or password:
            return make_response(
                {"message": "Invalid username or password"}, 400
            )

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return make_response(
                UserSchema().dump(user), 200
            )

        return make_response(
            {"error": "Login failed, incorrect username or password"}, 401
        )


class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None

            return make_response(
                {"message": "logged out successfully"}, 204
            )

        return make_response(
            {"error": "log out failed, you have no active sessions"}, 401
        )


# Resources routes
class Journals(Resource):
    pass

# Configure api routes
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Journals, '/journals')

if __name__ == '__main__':
    app.run(port=5555, debug=True)