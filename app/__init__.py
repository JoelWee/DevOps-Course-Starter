from flask import Flask
from flask_pymongo import PyMongo

from app.flask_config import Config
from app.routes import bp


def create_app(mongo_uri: str = None):
    app = Flask(__name__)
    app.config.from_object("app.flask_config.Config")
    if mongo_uri:
        app.config["MONGO_URI"] = mongo_uri

    if not app.config["MONGO_URI"]:
        raise ValueError("Missing config for Flask application")

    app.register_blueprint(bp)
    app.mongo = PyMongo(app)

    return app
