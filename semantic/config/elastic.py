from elasticsearch import Elasticsearch

from config.config import settings

client = Elasticsearch(
    [settings.ELASTIC_URL],
    basic_auth=(settings.ELASTIC_USERNAME, settings.ELASTIC_PASSWORD),
    request_timeout=60,
    ca_certs=settings.ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES
)

# Kiểm tra kết nối khi khởi động
# if client.ping():
#     print("✅ Connected to Elasticsearch!")
# else:
#     print("❌ Failed to connect to Elasticsearch!")
client.info()


