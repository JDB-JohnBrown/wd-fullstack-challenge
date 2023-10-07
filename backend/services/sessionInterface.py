# services\sessionInterface.py
# Based on https://medium.com/@andrelbaldo/register-login-and-logout-boilerplate-written-in-vue-js-and-python-as-api-5ce57e33774b

from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header

class SessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(SessionInterface, self).save_session(*args, **kwargs)

@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True