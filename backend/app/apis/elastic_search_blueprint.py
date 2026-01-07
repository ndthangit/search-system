from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi
from app.services.elastic_service import ElasticService
from app.dto.request.multi_match_search_request import MultiMatchSearchRequest
from app.dto.response.search_response import SearchResponse
from app.dto.response.hit_response import HitResponse
from app.dto.response.document_dto import DocumentDto

bp = Blueprint("elastic_search", url_prefix="/elastic_search")

es_service = ElasticService()

def _expand_search_fields(fields: list[str]) -> list[str]:
    expanded: list[str] = []
    for field in fields:
        if field == "title":
            expanded.extend(["title-va", "title-vska"])
        elif field == "summary":
            expanded.extend(["summary-va", "summary-vska"])
        else:
            expanded.append(field)

    seen: set[str] = set()
    result: list[str] = []
    for field in expanded:
        if field not in seen:
            seen.add(field)
            result.append(field)
    return result


@bp.get("/ping")
@openapi.summary("Check Elasticsearch connection")
@openapi.description("Ping Elasticsearch to check if it is running and reachable.")
@openapi.response(200, {"application/json": {"status": str}}, "Ping result")
async def ping(_):
    ok = await es_service.ping()
    return json({"status": "ok" if ok else "error"})

# @bp.post("/analyze")
# @openapi.summary("Analyze text")
# @openapi.description("Check how Elasticsearch tokenizes (splits) the input text.")
# @openapi.body(
#     {
#         "application/json": {
#             "text": str,
#             "field": str,
#         }
#     },
#     required=True,
#     description="Text and optional field name to analyze"
# )
# @openapi.response(200, {"application/json": {"tokens": list}}, "Tokenization result")
# async def analyze_text(request):
#     """
#     Gửi text tới Elasticsearch để xem nó tách từ (tokenize) thế nào.
#     """
#     data = request.json
#     text = data.get("text")
#     field = data.get("field", "content")

#     if not text:
#         return json({"error": "Missing 'text' in request body"}, status=400)

#     # Gọi ElasticService
#     res = await es_service.analyze_text("test-index", text, field)
#     return json(res.body)


@bp.post("/save-document/<index_name:str>")
@openapi.summary("Index document into Elasticsearch")
@openapi.description("Add or update a document in the 'articles' index.")
@openapi.body(
    {
        "application/json": {
            "id": str,
            "link": str,
            "title": str,
            "summary": str,
            "length": int,
            "last_updated": int
        }
    },
    required=True,
    description="Document to be indexed"
)
@openapi.response(200, {"application/json": {"result": str}}, "Index result")
async def index_data(request, index_name: str):
    data = request.json

    link = data.get("link")
    title = data.get("title")
    summary = data.get("summary")
    body = {
        "link": link,
        "title-va": title,
        "title-vska": title,
        "summary-va": summary,
        "summary-vska": summary,
        "length": data.get("length"),
        "last_updated": data.get("last_updated"),
    }

    res = await es_service.index_data(index_name, data.get("id"), body)
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

    fields = _expand_search_fields(body.fields)
    query = {
        "query": {
            "multi_match": {
                "query": body.query,
                "fields": fields
            }
        },
        "from": (body.page - 1) * body.size,
        "size": body.size
    }

    res = await es_service.search_match(index_name, query)
    hits = res['hits']['hits']
    total_elements = res['hits']['total']['value']
    total_pages = (total_elements + body.size - 1) // body.size
    took = res['took']
    max_score = res['hits'].get('max_score')

    response = SearchResponse(
        pageNumber=body.page,
        pageSize=body.size,
        totalElements=total_elements,
        totalPages=total_pages,
        took=took,
        maxScore=max_score,
        data=[
            HitResponse(
                index=hit["_index"],
                id=hit["_id"],
                score=hit.get("_score"),
                source=DocumentDto(**hit["_source"])
            )
            for hit in hits
        ]
    )

    return json(response.dict())
