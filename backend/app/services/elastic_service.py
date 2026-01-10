import os
from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError
from config import ElasticSearchConfig


class ElasticService:
    def __init__(self, host: str = ElasticSearchConfig.HOST):
        self.client = AsyncElasticsearch(
            hosts=[host],
            basic_auth=(
                ElasticSearchConfig.USERNAME,
                ElasticSearchConfig.PASSWORD
            )
        )

    async def ping(self) -> bool:
        return await self.client.ping()

    async def index_data(self, index: str, doc_id: str | None, body: dict): # doc_id None là tạo mới
        if doc_id:
            return await self.client.index(index=index, id=doc_id, document=body)
        else:
            return await self.client.index(index=index, document=body)

    async def search_match(self, index: str, body: dict):
        try:
            return await self.client.search(index=index, body=body)
        except NotFoundError:
            return {
                "hits": {
                    "total": {"value": 0, "relation": "eq"},
                    "hits": []
                }
            }

    # async def analyze_text(self, index, text, field):
    #     return await self.client.indices.analyze(
    #         index=index,
    #         body={
    #             "field": field,
    #             "text": text
    #         }
    #     )

    async def delete_doc(self, index: str, doc_id: str):
        await self.client.delete(index=index, id=doc_id, ignore=[404])

    async def close(self):
        await self.client.close()
