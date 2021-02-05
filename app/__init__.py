from flask import Flask
from flask_pymongo import PyMongo

from app.routes import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.flask_config.Config")
    app.register_blueprint(bp)
    app.mongo = PyMongo(app)

    return app
