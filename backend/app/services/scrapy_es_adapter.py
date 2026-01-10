import asyncio
from twisted.internet import defer

from app.services.elastic_service import ElasticService


class ScrapyElasticAdapter:
    def __init__(self):
        self._service = ElasticService()

    def search_match(self, index: str, body: dict):
        coro = self._service.search_match(index, body)
        return defer.Deferred.fromFuture(asyncio.ensure_future(coro))

    def index_data(self, index: str, doc_id: str | None, body: dict):
        coro = self._service.index_data(index, doc_id, body)
        return defer.Deferred.fromFuture(asyncio.ensure_future(coro))

    def delete_doc(self, index: str, doc_id: str):
        coro = self._service.delete_doc(index, doc_id)
        return defer.Deferred.fromFuture(asyncio.ensure_future(coro))

    async def close(self):
        if self._service:
            await self._service.close()
