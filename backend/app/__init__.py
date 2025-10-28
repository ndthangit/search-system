from sanic import Sanic

from config import Config


def register_extensions(sanic_app: Sanic):
    # CORs
    sanic_app.config.CORS_ORIGINS = "*"

    # OpenAPI swagger
    sanic_app.ext.openapi.add_security_scheme('Authorization', 'apiKey', location='header', name='Authorization')
    sanic_app.ext.openapi.raw(Config.raw)

def register_routes(sanic_app: Sanic):
    from app.apis import api

    sanic_app.blueprint(api)


def create_app(*config_cls) -> Sanic:
    sanic_app = Sanic(__name__)

    for config in config_cls:
        sanic_app.config.update_config(config)

    register_extensions(sanic_app)
    register_routes(sanic_app)

    return sanic_app