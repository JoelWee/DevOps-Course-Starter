"""Flask configuration class."""
import os


class Config:
    """Base configuration variables."""

    MONGO_URI = os.environ.get("MONGO_URI")
    OAUTH_CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    LOGIN_DISABLED = os.environ.get("LOGIN_DISABLED")
