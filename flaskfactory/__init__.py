__all__ = ["create_app", "db", "app"]

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import *

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    # db.create_all()

    from resources import api

    api.init_app(app)

    return app
