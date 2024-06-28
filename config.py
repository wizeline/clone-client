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
    S3_BUCKET = environ.get("S3_BUCKET")
    OPENSEARCH_INDEX = environ.get("OPENSEARCH_INDEX")
    OPENSEARCH_HOST = environ.get("OPENSEARCH_HOST")
    OPENSEARCH_PORT = environ.get("OPENSEARCH_PORT")
    OPENSEARCH_USE_SSL = environ.get("OPENSEARCH_USE_SSL")
    OPENSEARCH_VERIFY_CERTS = environ.get("OPENSEARCH_VERIFY_CERTS")
    IS_LOCAL = environ.get("IS_LOCAL")
    S3_URL = None
    S3_INDEX_PATH = environ.get("S3_INDEX_PATH")
    OPENSEARCH_USER = environ.get("OPENSEARCH_USER")
    OPENSEARCH_PASS = environ.get("OPENSEARCH_PASS")


class DevelopmentConfig(Config):
    """
    Development configuration
    """

    DEBUG = True
    LOG_LEVEL = "DEBUG"
    OPENSEARCH_CLUSTER_URL = "http://host.docker.internal:9200"
    OPENSEARCH_INDEX = "clone-vector-index"
    # OPENSEARCH_HOST = "localhost"
    OPENSEARCH_HOST = "host.docker.internal"
    OPENSEARCH_PORT = "9200"
    OPENSEARCH_USER = ""
    OPENSEARCH_PASS = ""
    OPENSEARCH_USE_SSL = False
    OPENSEARCH_VERIFY_CERTS = False
    S3_BUCKET = "clone-ingestion-messages"
    IS_LOCAL = True
    S3_URL = "http://host.docker.internal:4566"
    AWS_ACCESS_KEY_ID = "test"
    AWS_SECRET_ACCESS_KEY = "test"
    AWS_DEFAULT_REGION = "us-east-1"
    S3_INDEX_PATH = "/indexes"
