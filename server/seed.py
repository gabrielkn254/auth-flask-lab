from app import app
from models import db, User, Journal

with app.app_context():
    print("Deleting existing records...")
    print("Creating users...")
    print("Creating journals...")
    print("Committing users and documents to db...")
    print("Complete...")