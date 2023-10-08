#   services\propertyInterface
#   this module is for getting a user's listings, searching for other properties, and adding a property to a user

from sqlalchemy import and_, or_, update, insert
from models.databaseSessionManager import SessionManager
from models.property import Property
from models.property_link import User_Property_Link
from models.defaultMethodResult import DefaultMethodResult
from datetime import datetime
import json


class PropInterface():
        dbSession = SessionManager().session

        def createLink(self, user_id, property_id):
            error = None
            if error is None:
                newPLink = User_Property_Link(
                                user_id = user_id, 
                                property_id = property_id, 
                                create_date = datetime.now().timestamp())
                self.dbSession.add(newPLink)
                self.dbSession.commit()
                return DefaultMethodResult(True, 'User_PLink Created')
            
        def getListings(self, user_id):
            filtered = self.dbSession.query(Property).join(User_Property_Link, Property.property_id == User_Property_Link.property_id).filter(User_Property_Link.user_id == user_id).all()
            print("hi")
            print(filtered)
            results = [obj.to_dict() for obj in filtered]
            json_string = json.dumps(results)
            return json_string