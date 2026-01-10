from elasticsearch import Elasticsearch

from config.config import settings

client = Elasticsearch(
    [settings.ELASTIC_URL],
    basic_auth=(settings.ELASTIC_USERNAME, settings.ELASTIC_PASSWORD),
    request_timeout=60,
)
client.info()


