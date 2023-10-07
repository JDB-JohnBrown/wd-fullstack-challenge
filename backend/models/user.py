from flask_sqlalchemy import SQLAlchemy
import flask_login

db = SQLAlchemy()
class User(db.Model, flask_login.mixins.UserMixin):
    __tablename__ = 'user' # Name of the table in our database
    # Defining the columns
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passw = db.Column(db.String(120), unique=False, nullable=False)
    def get_id(self):
        return chr(self.user_id)