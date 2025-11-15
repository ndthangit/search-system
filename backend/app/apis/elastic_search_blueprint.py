from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi
from app.services.elastic_service import ElasticService
from app.dto.request.multi_match_search_request import MultiMatchSearchRequest
from app.dto.response.search_response import SearchResponse

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



INDEX_NAME = "articles"


@bp.post("/index")
@openapi.summary("Index document into Elasticsearch")
@openapi.description("Add or update a document in the 'articles' index.")
@openapi.body(
    {
        "application/json": {
            "id": str,
            "url": str,
            "title": str,
            "summary": str,
            "contents": str,
            "date": str,           # ISO8601
            "authors": [str],
            "category": str,
            "tags": [str]
        }
    },
    required=True,
    description="Document to be indexed"
)
@openapi.response(200, {"application/json": {"result": str}}, "Index result")
async def index_data(request):
    data = request.json
    doc_id = data.get("id")
    if not doc_id:
        return json({"error": "Missing 'id'"}, status=400)

    # Lấy nội dung chính
    contents = data.get("contents", "")

    # Chuẩn body index document
    body = {
        "url": data.get("url"),
        "title": data.get("title"),
        "summary": data.get("summary"),
        "contents": contents,
        "date": data.get("date"),
        "authors": data.get("authors", []),
        "category": data.get("category"),
        "tags": data.get("tags", []),
    }

    res = await es_service.index_data(INDEX_NAME, doc_id, body)
    return json(res.body)


@bp.post("/search-match/<index_name:str>")
@openapi.summary("Search documents with match query")
@openapi.description("Search documents using a multi-match query on the fields.")
@openapi.body(
    {"application/json": MultiMatchSearchRequest},
    required=True,
    description="Multi-match search request payload"
)
@openapi.response(200, {"application/json": SearchResponse}, "Search results")
async def search_match(request, index_name: str):
    """
    Tìm kiếm tài liệu sử dụng multi-match query trên các field được chỉ định.
    """
    data = request.json
    body = MultiMatchSearchRequest(**data) 

    query = {
        "query": {
            "multi_match": {
                "query": body.query,
                "fields": body.fields
            }
        },
        "from": (body.page - 1) * body.size,
        "size": body.size
    }

    res = await es_service.client.search_match(index=index_name, body=query)
    hits = res['hits']['hits']
    total_elements = res['hits']['total']['value']
    total_pages = (total_elements + body.size - 1) // body.size

    response = SearchResponse(
        pageNumber=body.page,
        pageSize=body.size,
        totalElements=total_elements,
        totalPages=total_pages,
        data=[hit for hit in hits]
    )

    return json(response.dict())