from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class User_Property_Link(db.Model):
    __tablename__ = 'user_property_link' # Name of the table in our database
    # Defining the columns
    user_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    property_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    create_date = db.Column(db.Integer, unique=False, nullable=False)