from flask_restx import fields


airport_schema = {
    "id": fields.Integer(readonly=True),
    "name": fields.String(),
    "city": fields.String(),
    "country": fields.String(),
    "iata": fields.String(),
    "icao": fields.String(),
    "latitude": fields.Float(),
    "longitude": fields.Float(),
    "altitude": fields.Integer(),
    "timezone": fields.Integer(),
    "DST": fields.String(),
    "tz": fields.String(),
    "type": fields.String(),
    "source": fields.String(),
    "deleted": fields.Integer()
}
