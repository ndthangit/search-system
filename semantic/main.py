from fastapi import FastAPI, HTTPException
from config.elastic import client
from model.elastis_model import SearchResponse, Document, SearchRequest

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
    try:
        # Perform semantic search using Elasticsearch
        search_body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": request.text,
                                "fields": ["name^2", "abstract", "content"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        },
                        {
                            "match": {
                                "name": {
                                    "query": request.text,
                                    "boost": 3
                                }
                            }
                        }
                    ]
                }
            },
            "size": 10,
            "_source": ["name", "abstract", "url"]
        }
        
        # Execute search
        response = client.search(
            index="documents",  # Replace with your actual index name
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
