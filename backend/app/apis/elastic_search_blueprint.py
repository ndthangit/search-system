from typing import Optional
from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi
from elasticsearch import NotFoundError
from app.services.elastic_service import ElasticService
from app.dto.request.multi_match_search_request import MultiMatchSearchRequest
from app.dto.response.search_response import SearchResponse
from app.dto.response.hit_response import HitResponse
from app.dto.response.document_dto import DocumentDto

bp = Blueprint("elastic_search", url_prefix="/elastic_search")

es_service = ElasticService()

def _expand_search_fields(fields: list) -> list:
    """
    Expand search fields from simplified names to Elasticsearch field names.
    
    Args:
        fields: List of field names ('title', 'content')
    
    Returns:
        List of Elasticsearch field names with optional boosting
    """
    if not fields:
        return ["content-va^2", "title-va"]
    
    mapping = {
        "title": "title-va",
        "content": "content-va"
    }
    
    return [mapping[field] for field in fields if field in mapping]

def build_highlight_summary(hit: dict, title_field: str = "title-va", content_field: str = "content-va") -> Optional[str]:
    highlight = hit.get("highlight")
    if not highlight:
        return None

    parts = []
    
    # Xử lý title highlight
    title_fragments = highlight.get(title_field)
    if title_fragments:
        if isinstance(title_fragments, list):
            parts.append(" ... ".join(title_fragments))
        else:
            parts.append(str(title_fragments))
    
    # Xử lý content highlight
    content_fragments = highlight.get(content_field)
    if content_fragments:
        if isinstance(content_fragments, list):
            parts.append(" ... ".join(content_fragments))
        else:
            parts.append(str(content_fragments))
    
    # Nối title và content với " ... "
    if parts:
        return " ... ".join(parts)
    
    return None


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
            "content": str,
            "length": int,
            "last_updated": str
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
    content = data.get("content")
    body = {
        "link": link,
        "title-va": title,
        "content-va": content,
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
                "fields": fields,
                "fuzziness": "AUTO",
                "type": "most_fields"
            }
        },
        "highlight": {
            "pre_tags": [
                "<strong>"
            ],
            "post_tags": [
                "</strong>"
            ],
            "fields": {
                "content-va": {
                    "number_of_fragments": 4,
                    "fragment_size": 50
                },
                "title-va":{
                    "number_of_fragments": 4,
                    "fragment_size": 50
                }
            }
        },
        "from": (body.page - 1) * body.size,
        "size": body.size
    }

    try:
        res = await es_service.search_match(index_name, query)
        hits = res['hits']['hits']
        total_elements = res['hits']['total']['value']
        total_pages = (total_elements + body.size - 1) // body.size
        took = res['took']
        max_score = res['hits'].get('max_score')
    except NotFoundError:
        hits = []
        total_elements = 0
        total_pages = 0
        took = None
        max_score = None

    data = []

    for hit in hits:
        doc = DocumentDto(**hit["_source"])

        highlight_summary = build_highlight_summary(hit, "title-va", "content-va")
        if highlight_summary:
            doc.content_va = highlight_summary   # ghi đè

        data.append(
            HitResponse(
                index=hit["_index"],
                id=hit["_id"],
                score=hit.get("_score"),
                source=doc
            )
        )

    response = SearchResponse(
        pageNumber=body.page,
        pageSize=body.size,
        totalElements=total_elements,
        totalPages=total_pages,
        took=took,
        maxScore=max_score,
        data=data
    )

    return json(response.dict())
