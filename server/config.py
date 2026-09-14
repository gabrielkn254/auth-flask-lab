import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# load .env files in os
load_dotenv()

# Create app
app = Flask(__name__)

# db configs
db_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# token configs
app_secret = os.getenv("APP_SECRET_KEY")
if not app_secret:
    raise RuntimeError("CRITICAL: `APP_SECRET_KEY` variable not set")

app.secret_key = app_secret
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)