"""Flask configuration class."""
import os


class Config:
    """Base configuration variables."""

    TRELLO_API_TOKEN = os.environ.get("TRELLO_API_TOKEN")
    TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")

    if not (TRELLO_API_KEY and TRELLO_API_TOKEN):
        raise ValueError(
            "Missing config for Flask application. Did you forget to run setup.sh?"
        )
