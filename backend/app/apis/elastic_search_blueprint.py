from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

bp = Blueprint(name='elastic_search', url_prefix='/elastic_search')


@bp.get('/')
async def get_asset_data(request: Request):
    return json({"message": "Elastic Search is running ..."})