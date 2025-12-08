import json as pyjson
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


def _build_document_body(data: dict) -> dict:
    return {
        "url": data.get("url"),
        "title": data.get("title"),
        "summary": data.get("summary"),
        "contents": data.get("contents"),
        "date": data.get("date"),
        "authors": data.get("authors", []),
        "category": data.get("category"),
        "tags": data.get("tags", []),
    }


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
async def index_data(request, index_name: str):
    data = request.json

    body = _build_document_body(data)

    res = await es_service.index_data(index_name, data.get("id"), body)
    return json(res.body)

## save in document by file json: is list data (use for iterate save one by one document)

@bp.post("/save-documents/<index_name:str>")
@openapi.summary("Index multiple documents from uploaded JSON file")
@openapi.description("Upload a JSON file containing an array of documents to be indexed one by one.")
@openapi.body(
    {
        "multipart/form-data": {
            "file": {
                "type": "string",
                "format": "binary",
                "description": "JSON file with a list of documents (same fields as single save)."
            }
        }
    },
    required=True,
    description="File upload with list of documents"
)
@openapi.response(
    200,
    {
        "application/json": {
            "indexed": int,
            "errors": list,
            "items": list
        }
    },
    "Bulk index result"
)
async def index_data_from_file(request, index_name: str):
    uploaded_files = request.files.get("file")
    if not uploaded_files:
        return json({"error": "Missing file in 'file' form field"}, status=400)

    uploaded_file = uploaded_files[0] if isinstance(uploaded_files, list) else uploaded_files

    try:
        documents = pyjson.loads(uploaded_file.body.decode("utf-8"))
    except Exception as exc:
        return json({"error": f"Invalid JSON file: {exc}"}, status=400)

    if not isinstance(documents, list):
        return json({"error": "JSON content must be a list of documents"}, status=400)

    indexed = []
    errors = []

    for doc in documents:
        if not isinstance(doc, dict):
            errors.append({"error": "Each item must be an object", "item": doc})
            continue

        body = _build_document_body(doc)

        try:
            res = await es_service.index_data(index_name, doc.get("id"), body)
            res_body = res.body if hasattr(res, "body") else res
            indexed.append(
                {
                    "id": res_body.get("_id"),
                    "result": res_body.get("result"),
                }
            )
        except Exception as exc:
            errors.append({"id": doc.get("id"), "error": str(exc)})

    status_code = 200 if not errors else 207
    return json({"indexed": len(indexed), "errors": errors, "items": indexed}, status=status_code)


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
