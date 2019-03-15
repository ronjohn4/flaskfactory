from app import db
from sqlalchemy import func


class StoreModel(db.Model):
    __tablename__ = 'store'

    # Fields
    name = db.Column(db.String(140), primary_key=True)
    active = db.Column(db.Boolean)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, name, active=False, lat=0, lng=0):
        # see discussion on key case sensitivity below in find_by_name()
        # I recommend using lower() on the incoming key parameter to keep the data consistent.
        # This creates a predictable state for other apps not using this API.
        self.name = name.lower()
        self.active = active
        self.lat = lat
        self.lng = lng

    def json(self):
        return {'name': self.name, 'active': self.active, 'lat': self.lat, 'lng': self.lng}

    @classmethod
    def find_by_name(cls, name):
        # This function is used by the HTTP verbs to locate an existing record by the unique key ('name' in
        # this example).  The API designer needs to decide if the key is case sensitive.
        #
        # I make the unique key case insensitive when possible based on the following:
        # 1. URIs are not case sensitive.  GOOGLE.COM and google.com resolve to the same endpoint.
        # 2. URIs have a loose association with folder paths on the server.
        # 3. Linux paths are case sensitive, though it is considered bad form to use 2 paths that vary by only case.
        # 4. Windows paths are case insensitive.
        # 5. Flask converts arguments to lower case by default (can be overridden).
        #
        # case sensitive
        # return cls.query.filter_by(name=name).first()
        #
        # case insensitive
        # The SQLAlchemy func.lower() function is used within the SQLAlchemy filter() function, ot python str.lower()
        return cls.query.filter(func.lower(cls.name) == func.lower(name)).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Store {}>'.format(self.name)
