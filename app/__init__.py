from flask import Flask
from flask_pymongo import PyMongo  # for Flask framework

from app.auth import bp as auth_bp
from app.auth import init_config_manager
from app.routes import bp as main_bp
from loggly.handlers import HTTPSHandler
from pythonjsonlogger import jsonlogger


def create_app(mongo_uri: str = None):
    app = Flask(__name__)
    app.config.from_object("app.flask_config.Config")
    if mongo_uri:
        app.config["MONGO_URI"] = mongo_uri

    if not app.config.get("MONGO_URI"):
        raise ValueError("Missing config for Flask application")

    init_config_manager(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.mongo = PyMongo(app)

    app.logger.setLevel(app.config["LOG_LEVEL"])
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(
            f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(
            jsonlogger.JsonFormatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)
    app.logger.info("App is up and running!")
    return app
