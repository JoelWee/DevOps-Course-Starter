"""Flask configuration class."""
import os


class Config:
    """Base configuration variables."""

    MONGO_URI = os.environ.get("MONGO_URI")

    if not MONGO_URI:
        raise ValueError("Missing config for Flask application")
