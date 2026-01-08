import os
from elasticsearch import AsyncElasticsearch

from config import ElasticSearchConfig


class ElasticService:
    def __init__(self, host: str = ElasticSearchConfig.HOST):
        ca_cert = ElasticSearchConfig.CA_CERT_PATH
        use_ssl = host.startswith('https') and os.path.exists(ca_cert)

        if use_ssl:
            self.client = AsyncElasticsearch(
                hosts=[host],
                basic_auth=(ElasticSearchConfig.USERNAME, ElasticSearchConfig.PASSWORD),
                ca_certs=ca_cert,
                verify_certs=True
            )
        else:
            self.client = AsyncElasticsearch(hosts=[host])

    async def ping(self) -> bool:
        return await self.client.ping()

    async def index_data(self, index: str, doc_id: str | None, body: dict): # doc_id None là tạo mới
        if doc_id:
            return await self.client.index(index=index, id=doc_id, document=body)
        else:
            return await self.client.index(index=index, document=body)

    async def search_match(self, index: str, body: dict):
        return await self.client.search(index=index, body=body)

    # async def analyze_text(self, index, text, field):
    #     return await self.client.indices.analyze(
    #         index=index,
    #         body={
    #             "field": field,
    #             "text": text
    #         }
    #     )

    async def close(self):
        await self.client.close()
