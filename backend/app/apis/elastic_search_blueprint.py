from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi
from app.services.elastic_service import ElasticService

bp = Blueprint("elastic_search", url_prefix="/elastic_search")

es_service = ElasticService()


@bp.get("/ping")
@openapi.summary("Check Elasticsearch connection")
@openapi.description("Ping Elasticsearch to check if it is running and reachable.")
@openapi.response(200, {"application/json": {"status": str}}, "Ping result")
async def ping(_):
    ok = await es_service.ping()
    return json({"status": "ok" if ok else "error"})


@bp.post("/index")
@openapi.summary("Index document into Elasticsearch")
@openapi.description("Add or update a document in the `test-index`.")
@openapi.body(
    {
        "application/json": {
            "id": str,
            "title": str,
            "content": str,
            "author": str,
            "tags": [str],
        }
    },
    required=True,
    description="Document to be indexed"
)
@openapi.response(200, {"application/json": {"result": str}}, "Index result")
async def index_data(request):
    data = request.json
    res = await es_service.index_data("test-index", data.get("id"), data)
    return json(res.body)


@bp.get("/search")
@openapi.summary("Search documents")
@openapi.description("Search documents in `test-index` using a query string.")
@openapi.parameter(
    name="q",
    description="Search query (matches against `content` field)",
    required=True,
    location="query",
    schema=str
)
@openapi.response(200, {"application/json": {"hits": list}}, "Search results")
async def search(request):
    query = request.args.get("q", "")
    res = await es_service.search("test-index", query)
    return json(res.body)

@bp.post("/analyze")
@openapi.summary("Analyze text")
@openapi.description("Check how Elasticsearch tokenizes (splits) the input text.")
@openapi.body(
    {
        "application/json": {
            "text": str,
            "field": str,
        }
    },
    required=True,
    description="Text and optional field name to analyze"
)
@openapi.response(200, {"application/json": {"tokens": list}}, "Tokenization result")
async def analyze_text(request):
    """
    Gửi text tới Elasticsearch để xem nó tách từ (tokenize) thế nào.
    """
    data = request.json
    text = data.get("text")
    field = data.get("field", "content")

    if not text:
        return json({"error": "Missing 'text' in request body"}, status=400)

    # Gọi ElasticService
    res = await es_service.analyze_text("test-index", text, field)
    return json(res.body)
