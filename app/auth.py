import os
from enum import Enum
from functools import wraps

import requests
from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_login import UserMixin, current_user, login_user
from flask_login.login_manager import LoginManager
from flask_login.mixins import AnonymousUserMixin
from flask_login.utils import login_required
from oauthlib.oauth2 import WebApplicationClient

authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
user_url = "https://api.github.com/user"

client = WebApplicationClient(os.environ.get("OAUTH_CLIENT_ID"))
if os.environ.get("FLASK_ENV") == "development" or True:  # Heroku has no ssl
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class Role(Enum):
    READER = "READER"
    WRITER = "WRITER"


roles = {"JoelWee": Role.WRITER.value}


def init_config_manager(app):
    login_manager = LoginManager()

    if app.config.get("LOGIN_DISABLED"):
        AnonymousUser.role = Role.WRITER.value
    login_manager.anonymous_user = AnonymousUser

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(url_for("auth.login"))

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)


bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@bp.route("/login", methods=["GET"])
def login():
    return redirect(client.prepare_request_uri(authorization_base_url))


@bp.route("/authorize", methods=["GET"])
def authorize():
    url, headers, body = client.prepare_token_request(
        token_url,
        authorization_response=request.url,
        client_secret=current_app.config["OAUTH_CLIENT_SECRET"],
    )
    r = requests.post(url, body, headers={**headers, "accept": "application/json"})
    client.parse_request_body_response(r.content)
    url, headers, body = client.add_token(user_url)

    r = requests.get(url, headers={**headers, "accept": "application/json"})
    user_data = r.json()
    user = User(user_data["login"])
    login_user(user)
    return redirect("/")


class User(UserMixin):
    def __init__(self, username: str):
        self.id = username
        self.role = roles.get(username, Role.READER.value)


class AnonymousUser(AnonymousUserMixin):
    role = Role.READER.value
    id = "AnonymousUser"


def action_allowed(current_role: str, required_role: Role):
    if required_role == Role.WRITER:
        return current_role == Role.WRITER.value
    elif required_role == Role.READER:
        return current_role == Role.READER.value or current_role == Role.WRITER.value
    return True


def requires_role(required_role: Role):
    def decorator(func):
        @login_required
        @wraps(func)
        def with_authorization(*args, **kwargs):
            if not action_allowed(current_user.role, required_role):
                flash("Your role does not allow you to do this")
                return None
            return func(*args, **kwargs)

        return with_authorization

    return decorator
