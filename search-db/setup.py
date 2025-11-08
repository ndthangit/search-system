from elasticsearch import Elasticsearch

from elastic_custom_template.analyzer import AnalyzerComponent, AnalyzerCustom

client = Elasticsearch(
    hosts=["https://localhost:9200"],  # Địa chỉ Elasticsearch
    basic_auth=("elastic", "elastic"),
    request_timeout=60,
    ca_certs="./ca.crt"
)
client.info()



nfd_analyzer = AnalyzerCustom(
    name="nfd_normalized",
    tokenizer="icu_tokenizer"
)
nfd_analyzer.add_char_filters(["nfd_normalizer"])
# Không gọi set_explicit_type()

# 2. Tạo analyzer "vi_ngram_analyzer"
#    (Loại custom này CÓ "type": "custom" tường minh)
vi_ngram_analyzer = AnalyzerCustom(
    name="vi_ngram_analyzer",
    tokenizer="vi_ngram_tokenizer"
)
vi_ngram_analyzer.add_filters(["lowercase", "asciifolding"])
vi_ngram_analyzer.set_explicit_type()  # Đánh dấu để thêm type

# 3. Tạo AnalyzerComponent
analyzer_component = AnalyzerComponent()

# 4. Thêm các analyzer vào component
analyzer_component.add_analyzer(nfd_analyzer)
analyzer_component.add_analyzer(vi_ngram_analyzer)

# 5. Build từ điển cuối cùng
built_analyzers = analyzer_component.build()
print(built_analyzers)



index_template = {
    "index_patterns": ["articles*"],


    "template": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "60s",
            "translog.durability": "async",
            "translog.sync_interval": "30s",
            "merge.scheduler.max_thread_count": 1,
            "indexing.slowlog.threshold.index.warn": "10s",
            "indexing.slowlog.threshold.index.info": "5s",
            "analysis":built_analyzers
        },
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text"},
                "summary": {"type": "text"},
                "contents": {"type": "text"},
                "date": {"type": "date"},
                "authors": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}}
                },
                "category": {"type": "keyword"},
                "tags": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}}
                }
            }
        }
    }
}
print(index_template)


if client.indices.exists_index_template(name="baolaodong_template"):
    client.indices.delete_index_template(name="baolaodong_template")

client.indices.put_index_template(
    name="baolaodong_template",
    index_patterns=index_template['index_patterns'],
    template=index_template['template']
)

