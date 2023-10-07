from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class UserSession(SQLAlchemy().Model):
    __tablename__ = 'user_session' # Name of the table in our database
    # Defining the columns
    user_session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    login_date = Column(Integer, nullable=False)
    expire_date = Column(Integer, nullable=False)
    logged_out = Column(Boolean, nullable=False)
    jwToken = Column(String(4000), nullable=False)
    url = Column(String(4000), nullable=False)
    logout_date = Column(Integer, nullable=False)