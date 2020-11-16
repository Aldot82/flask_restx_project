from app.db import db, BaseModelMixin


class Airport(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    iata = db.Column(db.String(100), nullable=True)
    icao = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    altitude = db.Column(db.Integer, nullable=True)
    timezone = db.Column(db.Integer, nullable=True)
    DST = db.Column(db.String(100), nullable=True)
    tz = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    source = db.Column(db.String(100), nullable=True)
    deleted = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Airport, self).__init__(**kwargs)

    def __repr__(self):
        return f'{self.name} of {self.city}'

    def __str__(self):
        return f'{self.name}'
