from elasticsearch import AsyncElasticsearch

from config import ElasticSearchConfig


class ElasticService:
    def __init__(self, host: str = ElasticSearchConfig.HOST):
        self.client = AsyncElasticsearch(hosts=[host])

    async def ping(self) -> bool:
        return await self.client.ping()

    async def index_data(self, index: str, doc_id: str, body: dict):
        return await self.client.index(index=index, id=doc_id, document=body)

    async def search(self, index: str, query: str):
        body = {
            "query": {
                "match": {
                    "content": query
                }
            }
        }
        return await self.client.search(index=index, body=body)

    async def analyze_text(self, index, text, field):
        return await self.client.indices.analyze(
            index=index,
            body={
                "field": field,
                "text": text
            }
        )

    async def close(self):
        await self.client.close()
