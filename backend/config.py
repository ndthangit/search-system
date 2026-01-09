# python
import os


class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')
    WORKERS = int(os.getenv('SERVER_WORKERS', 1))
    HOST = os.getenv('SERVER_HOST', 'localhost')
    PORT = int(os.getenv('SERVER_PORT', 8080))

    RUN_SETTING = {
        'host': HOST,
        'port': PORT,
        'debug': DEBUG,
        'access_log': False,
        'auto_reload': DEBUG and WORKERS == 1,
        'workers': WORKERS
    }

    SERVER_NAME = os.getenv('SERVER_NAME') or f'http://{HOST}:{PORT}'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    RESPONSE_TIMEOUT = 300

    raw = {}
    if SERVER_NAME:
        raw['servers'] = [{'url': SERVER_NAME}]

    FALLBACK_ERROR_FORMAT = 'json'

    OAS_UI_DEFAULT = 'swagger'
    SWAGGER_UI_CONFIGURATION = {
        'apisSorter': "alpha",
        'docExpansion': "list",
        'operationsSorter': "alpha"
    }

    API_HOST = os.getenv('API_HOST', f'http://{HOST}:{PORT}')
    API_BASEPATH = os.getenv('API_BASEPATH', '')
    API_SCHEMES = os.getenv('API_SCHEMES', 'http')
    API_VERSION = os.getenv('API_VERSION', '0.0.1')
    API_TITLE = os.getenv('API_TITLE', 'Elastic Search API')
    API_DESCRIPTION = os.getenv('API_DESCRIPTION', 'Swagger for Elastic Search API')
    API_CONTACT_EMAIL = os.getenv('API_CONTACT_EMAIL', 'example@gmail.com')

class ElasticSearchConfig:
    HOST = os.getenv('ELASTICSEARCH_HOST', 'http://localhost:9200')
    USERNAME = os.getenv('ELASTICSEARCH_USERNAME', 'elastic')
    PASSWORD = os.getenv('ELASTIC_PASSWORD', 'elastic')
    CA_CERT_PATH = os.getenv('ELASTICSEARCH_CA_CERT', '/app/certs/ca/ca.crt')