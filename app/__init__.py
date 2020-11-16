from flask import Flask
from flask_restx import Api
from app.db import db
#from app.airports.api.resources import ariport_bp
from .ext import ma, migrate
from app.airports.api.resources import api as ns


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.url_map.strict_slashes = False
    api = Api(app, version='1.0', title='Airports API',
              description='API to work with airports worldwide')
    api.add_namespace(ns)
    return app
