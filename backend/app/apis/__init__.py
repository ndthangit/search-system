from sanic import Blueprint
from app.apis.elastic_search_blueprint import bp as elastic_search_bp


api = Blueprint.group(
    elastic_search_bp,
    url_prefix='/'
)