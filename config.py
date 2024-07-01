from os import environ

from dotenv import load_dotenv

load_dotenv()


IS_LOCAL = environ.get("IS_LOCAL")


class Config:
    """
    Configuration class
    """

    DEBUG = environ.get("DEBUG")
    LOG_LEVEL = environ.get("LOG_LEVEL")
    IS_LOCAL = environ.get("IS_LOCAL")
    VECTOR_SEARCH_URL = environ.get("VECTOR_SEARCH_URL")


class DevelopmentConfig(Config):
    """
    Development configuration
    """

    DEBUG = True
    LOG_LEVEL = "DEBUG"
    IS_LOCAL = True
    VECTOR_SEARCH_URL = environ.get("VECTOR_SEARCH_URL")
    AWS_ACCESS_KEY_ID = "test"
    AWS_SECRET_ACCESS_KEY = "test"
    AWS_DEFAULT_REGION = "us-east-1"
