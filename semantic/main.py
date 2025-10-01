from fastapi import FastAPI, HTTPException
from config.elastic import client
from model.elastis_model import SearchResponse, Document, SearchRequest
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def check_elasticsearch():
    """Kiểm tra kết nối Elasticsearch"""
    return {"status": "connected"} if client.ping() else {"status": "failed"}

@app.post("/search", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """
    Semantic search API using Elasticsearch
    """

    query_vector = model.encode(request.text).tolist()

    try:
        # Perform semantic search using Elasticsearch
        search_body = {
            "knn": [
                {
                    "field": "name_embedding",
                    "query_vector": query_vector,
                    "k": 10,
                    "num_candidates": 10,
                    "boost": 0.5  # Điều chỉnh trọng số cho từng field
                },
                {
                    "field": "abstract_embedding",
                    "query_vector": query_vector,
                    "k": 10,
                    "num_candidates": 10,
                    "boost": 0.3
                },
                {
                    "field": "full_text_embedding",
                    "query_vector": query_vector,
                    "k": 10,
                    "num_candidates": 10,
                    "boost": 0.2
                }
            ],
            "size": 10,
            "_source": ["name", "abstract", "url"]
        }

        # Execute search
        response = client.search(
            index="wikipedia-people-sample-embedding",  # Replace with your actual index name
            body=search_body
        )

        # Process results
        documents = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            documents.append(Document(
                name=source.get('name', ''),
                abstract=source.get('abstract', ''),
                url=source.get('url', '')
            ))

        return SearchResponse(
            success=True,
            list_docs=documents
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
