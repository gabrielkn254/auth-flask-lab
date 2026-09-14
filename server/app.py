from flask import make_response, request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Journal, UserSchema, JournalSchema


# home route
class Home(Resource):
    def get(self):

        return make_response(
            {"message": "welcome to Journal",
             "--help": {
                 "Login": "POST /login",
                 "Logout": "DELETE /logout",
                 "Signup": "POST /signup",
                 "Check session": "GET /check_session",
                 "View all journals": "GET /<username>/journals",
                 "Add a new journal": "POST /<username>/journals",
                 "View a single journal": "GET /<username>/journals/<int:journal_id>",
                 "Update journal": "PATCH /<username>/journals/<int:journal_id>",
                 "Delete journal": "DELETE /<username>/journals/<int:journal_id>",
             }}, 200
        )

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
    def get(self, username):
        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response({"error": "user not found"}, 404)
        
        user_journals = [JournalSchema().dump(journal) for journal in user.journals]

        return make_response(
            user_journals, 200
        )

    def post(self, username):
        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response({"error": "user not found"}, 404)
        
        request_json = request.get_json(silent=True)

        journal = Journal(
            title=request_json.get('title'),
            content=request_json.get('content'),
            user_id=user.id
        )

        try:
            db.session.add(journal)
            db.session.commit()

            return make_response(JournalSchema().dump(journal), 201)

        except IntegrityError:
            return make_response(
                {"error": "Unprocessable Entity"}, 422
            )


class SingleJournal(Resource):
    def get(self, username, id):
        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response({"error": "user not found"}, 404)

        journal = next((journal for journal in user.journals if journal.id == id), None)

        if not journal:
            return make_response({"error": "journal not found"}, 404)
        
        return make_response(
            JournalSchema().dump(journal), 200
        )

    def patch(self, username, id):
        # query user
        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response({"error": "user not found"}, 404)

        # query journal
        journal = next((journal for journal in user.journals if journal.id == id), None)

        if not journal:
            return make_response({"error": "journal not found"}, 404)

        # retrieve json from request
        request_json = request.get_json(silent=True)

        # patch updates
        journal.title=request_json.get('title', journal.title)
        journal.content=request_json.get('content', journal.title)

        # update database
        try:
            db.session.add(journal)
            db.session.commit()

            return make_response(JournalSchema().dump(journal), 200)

        except IntegrityError:
            return make_response(
                {"error": "Unprocessable Entity"}, 422
            )

    def delete(self, username, id):
        # query user
        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response({"error": "user not found"}, 404)

        # query journal
        journal = next((journal for journal in user.journals if journal.id == id), None)

        if not journal:
            return make_response({"error": "journal not found"}, 404)

        # delete journal
        db.session.delete(journal)
        db.session.commit()

        return make_response(
            {"message": "Journal deleted successfully"}, 200
            )


# only allowed logged in users to access their journals
@app.before_request
def check_if_logged_in():
    if request.endpoint in ['journals', 'single_journal']:

        username = request.view_args.get('username')

        # Check if username exists
        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response(
                {"error": "user not found"}, 404
            )

        # Check if user is logged in
        if not session.get('user_id'):
            return make_response(
                {"error": "Unauthorized"}, 401
            )

        # Check if logged-in user matches the username in the URL
        if session['user_id'] != user.id:
            return make_response(
                {"error": "Unauthorized"}, 401
            )


# Configure api routes
api.add_resource(Home, '/', endpoint='home')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Journals, '/<username>/journals', endpoint='journals')
api.add_resource(SingleJournal, '/<username>/journals/<int:id>', endpoint='single_journal')

if __name__ == '__main__':
    app.run(port=5555, debug=True)