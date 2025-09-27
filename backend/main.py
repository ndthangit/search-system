from fastapi import FastAPI
from config.elastic import client

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def check_elasticsearch():
    """Kiểm tra kết nối Elasticsearch"""
    return {"status": "connected"} if client.ping() else {"status": "failed"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
