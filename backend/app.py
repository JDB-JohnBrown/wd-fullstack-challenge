# app.py
# Author: John Brown
# Heavily references: https://medium.com/@andrelbaldo/register-login-and-logout-boilerplate-written-in-vue-js-and-python-as-api-5ce57e33774b
# Holds our API routes

import flask 
from flask import jsonify, request, session, redirect

from services.authenticate import Auth
from models.defaultMethodResult import DefaultMethodResult
from models.loginTokenResult import LoginTokenResult
from services.jsonClassEncoder import JsonClassEncoder
from services.propertyInterface import PropInterface

import flask_login
from flask_login import user_loaded_from_header
from services.sessionInterface import SessionInterface

from pprint import pprint

app = flask.Flask(__name__)
ALOWED_CORS_DOMAIN = 'http://localhost:8080'
app.secret_key = "WalkerDunlop2023-10-07JohnBrown"
jsonClassEncoder = JsonClassEncoder()

login_manager  = flask_login.LoginManager()
login_manager.init_app(app)

# services/sessionInterface/SessionInterface
app.session_interface = SessionInterface()

# services/authenticate/Auth
authModule = Auth()

# serices/propertyInterface/PropInterface
propInterface = PropInterface()

@login_manager.user_loader
def load_user(user_id):
    return authModule.load_user(user_id)

# Only requests that have an Authorization request reader set with a valid login token
# can access the protected routes, like this '/home' one for example
@app.route('/home', methods=(['GET']))
@flask_login.login_required
def home():
    return 'Home protected by @flask_login.login_required'

# Sets the route for this endpoint, this will configure our web server to receive requests at this path.
@app.route('/register', methods=(['POST']))
def register():
    requestPayload = request.get_json()  
    username = requestPayload['username']
    password = requestPayload['password']

    registerResult = authModule.register(username, password)
    if registerResult.success == True:
        return jsonClassEncoder.encode(registerResult), 200
    else:
        return jsonClassEncoder.encode(registerResult), 500
    
# this route will login the user and return a Json Web Token, this token 
# will be stored into the client aplication and need to be passed over for each new 
# request, via Authorizaton header.
@app.route('/token', methods=(['POST']))
def token():
    authToken = request.headers.get('Authorization')
    activeSession = authModule.GetActiveSession(authToken)
    if activeSession is not None:
        loginResult = LoginTokenResult(True, 'Login successful', activeSession.jwToken)
        return jsonClassEncoder.encode(loginResult), 200
    else:
        requestPayload = request.get_json()  
        username = requestPayload['username']
        password = requestPayload['password']
        loginResult = authModule.getLoginToken(username, password, app.config['SECRET_KEY'])
        if loginResult.success == True:
            return jsonClassEncoder.encode(loginResult), 200
        else:
            return jsonClassEncoder.encode(loginResult), 401

# This will invalidate the user current user session on the server
@app.route('/logout', methods=(['POST']))
def sessionLogout():
    authToken = request.headers.get('Authorization')
    logoutResult = authModule.SessionLogout(authToken, request.url)
    if logoutResult.success == True:        
        return jsonClassEncoder.encode(logoutResult), 200
    else:
        return jsonClassEncoder.encode(logoutResult), 401


# This enable CORS, it means that this server will authorize AJAX calls from
# other domains than the current domain where the API is running
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = ALOWED_CORS_DOMAIN
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers

    return response
app.after_request(add_cors_headers)


# Checks if the user is auhenticated for protected routes decorated with @flask_login.login_required
@login_manager.request_loader
def load_user_from_request(request):
    # Get the token from the Authorization request header 
    authToken = request.headers.get('Authorization')
    if authToken:
        try:
            # Checks if is there a active session for this token and return his user
            user = authModule.GetUserByToken(authToken)
            return user
        except TypeError:
            pass        

    # If it can't find an active session returns None, 
    # this will cause the request decorated with @flask_login.login_required been denied
    return None

@app.route('/getUserListings', methods=(['GET']))
@flask_login.login_required
def getUserListings():
    user = load_user_from_request(request)
    listings = propInterface.getListings(user.user_id)
    print("JOHN!")
    pprint(listings)
    return listings

app.run()    