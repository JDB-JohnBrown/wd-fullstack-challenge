#   services\authenticate
#   this module logs users in & does authentication checks

from passlib.hash import sha256_crypt
import jwt
from models.user import User
from models.user_session import UserSession
from models.databaseSessionManager import SessionManager
from models.defaultMethodResult import DefaultMethodResult
from models.loginTokenResult import LoginTokenResult
from datetime import datetime, timedelta

from sqlalchemy import and_, or_, update


JWT_EXP_DELTA_SECONDS = 20
SESSION_TIMEOUT_IN_HOURS = 24

class Auth():
        dbSession = SessionManager().session
        def register(self, username, password) -> DefaultMethodResult:
            """
            This method will validate the data and create a new registration
            into our database.
            """

            # checks that the username/password are valid
            error = self.validateRefisterData(username, password)

            # lets hash our password using PassLib
            password = sha256_crypt.encrypt(password)

            if error is None:
                newUser = User(username = username, password = password)
                self.dbSession.add(newUser)
                self.dbSession.commit()
                return DefaultMethodResult(True, 'User Created')
            
            # error had a value, return false
            return DefaultMethodResult(False, error)
        
        def validateRegisterData(self, username, password) -> LoginTokenResult:
            """
            Check if the username is not blank, and not already in use. Minimum of 4 characters
            Check that password is a minimum of seven characters
            they are not correct.
            """

            # Define some sets so I can check the password mets the requirments easily. 
            # Could also do this with regex, and keep myself from typing out all the numbers,
            #       but I think regex isn't as simple to read
            specialCharacters = set('$#@!*')
            digits = set('0123456789')
            lCase = set('abcdefghijklmnopqrstuvwxyz')
            uCase = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


            error = None
            # The condition if not checks for None or empty values.
            if not username:
                error = 'Username is required.'
            # Also checks the password for None or empty values
            elif not password:
                error = 'Password is required.'
                

            if len(password) < 7:
                error = 'Password length is less than 8.'

            if not specialCharacters.intersection(password):
                if len(error) > 0:
                    error += "<br>"
                error = 'Your password must have at least 1 special character ($, #, @, !, *)'

            if not lCase.intersection(password):
                if len(error) > 0:
                    error += "<br>"
                error = 'Your password must have at least 1 lowercase character'
            
            if not uCase.intersection(password):
                if len(error) > 0:
                    error += "<br>"
                error = 'Your password must have at least 1 uppsercase character'
            
            # Query our database to check if the username is already registred
            result = self.dbSession.query(User).filter_by(username=username).first()
            # If the result returns some user sets an error
            if result is not None:
                error = 'Username {} is already in use.'.format(username)

            return error
        def getLoginToken(self, username, password, appSecret):
            """
            It does some basic validations first and then checks if the password
            matches with the one stored into the database, case the credentials
            were accepted a login token is created onto the database and returned.
            """
            error = None
            # The condition if not checks for None or empty values.
            if not username:
                error = 'Username is required.'
            # Also checks the password for None or empty values
            elif not password:
                error = 'Password is required.'
            # Query our database to check username exists
            result = self.dbSession.query(User).filter_by(username=username).first()
            if result is None:
                error = 'Invalid credentials'
            else:
                # I'm using PassLib.sha256_crypt for all passwords
                if sha256_crypt.verify(result.password, password) == False:
                    error = 'Invalid credentials'

            success = False
            if error is None:
                success = True
                payload = {
                    'userId': result.userId,
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
                jwt_token = jwt.encode(payload, appSecret,algorithm='HS256')
                #decodedToken = jwt.decode(jwt_token, appSecret, algorithms=['HS256'])
                jwtDecoded = jwt_token.decode("utf-8")
                self.createUserSessionOnDatabase(result.userId, jwtDecoded)
                return LoginTokenResult(success, 'login result', jwtDecoded)
            else:
                return LoginTokenResult(False, error, '')
            
        def createUserSessionOnDatabase(self, userId, jwToken):
            """
            Adds a new register into UserSession table to keep the user session 
            active until it expires or revoked via logout
            """
            userSession = UserSession(
                user_id = userId,
                logged_out = False,
                login_date = datetime.now().timestamp(),
                expire_date = (datetime.now() + timedelta(hours=SESSION_TIMEOUT_IN_HOURS)).timestamp(), 
                jwToken=jwToken
            )
            self.dbSession.add(userSession)
            self.dbSession.commit()

        def load_user(self, user_id):
            return self.dbSession.query(User).get(int(user_id))
        
        def GetUserByEmail(self, email):
            return self.dbSession.query(User).filter_by(username=email).first()
        
        def GetUserByToken(self, jwt):
            filtered = self.dbSession.query(UserSession).order_by(UserSession.userSessionId).filter(
            and_(UserSession.jwToken==jwt ,UserSession.expireDate > datetime.now(), UserSession.loggedOut == False)
            )
            activeSession = filtered.first()

            if activeSession is not None:
                return self.dbSession.query(User).get(activeSession.userId)
            else:
                return None
            
        def SessionLogout(self, jwt, url):
            """
            Sets the session as logged out and set the logoutDate.
            """
            if jwt is not None:
                currentUserSession = self.dbSession.query(UserSession).filter_by(jwToken=jwt).first()
                if currentUserSession is not None:
                    if currentUserSession.logged_out == False:
                        currentUserSession.logged_out = True
                        currentUserSession.logout_date = datetime.now().timestamp()
                        currentUserSession.url = url
                        self.dbSession.commit()
                    return DefaultMethodResult(True, 'Logout completed')
            
            return DefaultMethodResult(False, 'Error trying to logout')
        
        def GetActiveSession(self, jwt):
            """
            Returns an active login session for the given JWToken, if it exists.
            """
            if jwt is not None:
                currentUserSession = self.dbSession.query(UserSession).filter_by(jwToken=jwt).first()
                if currentUserSession is not None:
                    if currentUserSession.loggedOut == False:
                        return currentUserSession
            return None
