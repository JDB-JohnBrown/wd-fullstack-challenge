from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class Property(db.Model):
    __tablename__ = 'property' # Name of the table in our database
    # Defining the columns
    property_id = db.Column(db.Integer, primary_key=True)
    full_address = db.Column(db.String(256), unique=False, nullable=False)
    class_description = db.Column(db.String(256), unique=False, nullable=True)
    estimated_market_value = db.Column(db.String(32), unique=False, nullable=True)
    bldg_use = db.Column(db.String(32), unique=False, nullable=True)
    building_sq_ft = db.Column(db.String(32), unique=False, nullable=True)

    def to_dict(self):
        return {"property_id": self.property_id, 
                "full_address": self.full_address,
                "class_description": self.class_description,
                "estimated_market_value": self.estimated_market_value,
                "bldg_use": self.bldg_use,
                "building_sq_ft": self.building_sq_ft
                }