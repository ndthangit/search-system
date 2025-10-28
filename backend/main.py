from sanic import redirect, Request
from sanic_ext import openapi

from app import create_app
from config import Config

app = create_app(Config)


@app.get("/")
@openapi.exclude()
@openapi.tag("Ping")
@openapi.summary("Base URL")
async def hello_world(request: Request):
    if not Config.SERVER_NAME:
        docs_url = '/docs'
    elif Config.SERVER_NAME.endswith('/'):
        docs_url = f'{Config.SERVER_NAME}docs'
    else:
        docs_url = f'{Config.SERVER_NAME}/docs'

    return redirect(docs_url)


if __name__ == '__main__':
    try:
        app.run(**app.config['RUN_SETTING'])
    except (KeyError, OSError):
        print('End Server...')
