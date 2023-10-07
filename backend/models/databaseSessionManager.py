# models\databaseSessionManager
# adapted from: https://medium.com/@andrelbaldo/register-login-and-logout-boilerplate-written-in-vue-js-and-python-as-api-5ce57e33774b
# changed to use sqlite database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///wd-fsc.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)

class SessionManager(object):
    def __init__(self):
        self.session = Session()