from fastapi import FastAPI, HTTPException, Request
from config.elastic import client
from model.elastis_model import SearchResponse, Document, SearchRequest
from sentence_transformers import SentenceTransformer
import logging
import psutil
import time
from datetime import datetime
import sys
from fastapi.middleware.cors import CORSMiddleware

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# Enhanced logging configuration for terminal output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Ensure output goes to terminal
    ]
)

# Create logger instances for different components
logger = logging.getLogger(__name__)
system_logger = logging.getLogger('system')
request_logger = logging.getLogger('request')
elastic_logger = logging.getLogger('elasticsearch')

# Log system startup information
logger.info('🚀 Starting FastAPI server...')
logger.info(f'Python version: {sys.version}')
logger.info(f'Platform: {sys.platform}')

# Log initial system information
def log_system_info():
    """Log current system information"""
    try:
        # CPU information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory information
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        memory_used_gb = memory.used / (1024**3)
        memory_percent = memory.percent
        
        # Disk information
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024**3)
        disk_used_gb = disk.used / (1024**3)
        disk_percent = (disk.used / disk.total) * 100
        
        system_logger.info(f'💻 System Info - CPU: {cpu_percent}% ({cpu_count} cores)')
        system_logger.info(f'🧠 Memory: {memory_used_gb:.1f}GB/{memory_gb:.1f}GB ({memory_percent}%)')
        system_logger.info(f'💾 Disk: {disk_used_gb:.1f}GB/{disk_total_gb:.1f}GB ({disk_percent:.1f}%)')
        
    except Exception as e:
        system_logger.error(f'Failed to get system info: {e}')

# Log initial system information
log_system_info()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    request_logger.info(f'📥 {request.method} {request.url.path} - Client: {request.client.host if request.client else "unknown"}')
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    request_logger.info(f'📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s')
    
    return response

@app.get("/")
async def root():
    logger.info('🏠 Root endpoint accessed')
    return {"message": "Hello World"}

@app.get("/health")
def check_elasticsearch():
    """Kiểm tra kết nối Elasticsearch"""
    elastic_logger.info('🔍 Checking Elasticsearch connection...')
    
    try:
        is_connected = client.ping()
        if is_connected:
            elastic_logger.info('✅ Elasticsearch connection successful')
            return {"status": "connected"}
        else:
            elastic_logger.warning('❌ Elasticsearch connection failed')
            return {"status": "failed"}
    except Exception as e:
        elastic_logger.error(f'❌ Elasticsearch connection error: {e}')
        return {"status": "error", "message": str(e)}

@app.post("/search", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """
    Semantic search API using Elasticsearch
    """
    search_start_time = time.time()
    logger.info(f'🔍 Starting semantic search for query: "{request.text[:50]}..."')
    
    try:
        # Log system info before processing
        log_system_info()
        
        # Encode query to vector
        encode_start = time.time()
        query_vector = model.encode(request.text).tolist()
        encode_time = time.time() - encode_start
        logger.info(f'🧠 Query encoded in {encode_time:.3f}s (vector length: {len(query_vector)})')

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
        elastic_logger.info('🔍 Executing Elasticsearch query...')
        search_start = time.time()
        response = client.search(
            index="wikipedia-people-sample-embedding",  # Replace with your actual index name
            body=search_body
        )
        search_time = time.time() - search_start
        elastic_logger.info(f'✅ Elasticsearch query completed in {search_time:.3f}s')

        # Process results
        process_start = time.time()
        documents = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            documents.append(Document(
                name=source.get('name', ''),
                abstract=source.get('abstract', ''),
                url=source.get('url', '')
            ))
        process_time = time.time() - process_start
        
        total_time = time.time() - search_start_time
        
        logger.info(f'📊 Search completed - Found {len(documents)} results')
        logger.info(f'⏱️  Timing - Encode: {encode_time:.3f}s, Search: {search_time:.3f}s, Process: {process_time:.3f}s, Total: {total_time:.3f}s')
        
        # Log system info after processing
        log_system_info()

        return SearchResponse(
            success=True,
            list_docs=documents
        )

    except Exception as e:
        logger.error(f'❌ Search error: {str(e)}')
        elastic_logger.error(f'❌ Elasticsearch error: {str(e)}')
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


