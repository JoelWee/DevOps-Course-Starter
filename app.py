from flask import Flask

from routes import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("flask_config.Config")
    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    create_app().run()
