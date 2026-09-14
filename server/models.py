from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from marshmallow import Schema, fields

# set naming convections
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# create db
db = SQLAlchemy(metadata=metadata)

# models
class User(db.Model):
    __tablename__ = 'users'

    pass

class Journal(db.Model):
    __tablename__ = 'journals'
    pass


# schemas
class UserSchema(Schema):
    pass

class JournalSchema(Schema):
    pass