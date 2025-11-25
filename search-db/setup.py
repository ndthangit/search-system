import json

from elasticsearch import Elasticsearch

from elastic_custom_template.analysis import AnalysisComponent
from elastic_custom_template.analyzer import  AnalyzerCustom
from elastic_custom_template.filter import FilterStop, FilterComponent, Filter, FilterDictionaryDecompounder
from elastic_custom_template.tokenizer import TokenizerNgram

client = Elasticsearch(
    hosts=["https://localhost:9200"],  # Địa chỉ Elasticsearch
    basic_auth=("elastic", "elastic"),
    request_timeout=60,
    ca_certs="./ca.crt"
)
client.info()


# --- Tạo filter stopwords từ file ---

with open('data/stop_word.txt', 'r', encoding='utf-8') as file:
    words = [line.strip() for line in file if line.strip()]
print(words)
# # 2. Tạo các instance filter cụ thể
vi_stopwords = FilterStop(name="vi_stopwords", stopwords=words)

filter_component = FilterComponent()

filter_component.add_filter(vi_stopwords)
built_filters = filter_component.build()
print(built_filters)


vi_ngram_tokenizer = TokenizerNgram(
    name="vi_ngram_tokenizer",
    min_gram=2,
    max_gram=3,
    token_chars=["letter","digit","whitespace"]
)

analysis_settings = AnalysisComponent()

analysis_settings.filter_component.add_filter(vi_stopwords)

vi_dictionary_decompounder= FilterDictionaryDecompounder(name="vi_dictionary_decompounder",word_list=[
          "xã hội",
          "cộng hòa",
          "chủ nghĩa",
          "cánh đồng",
          "nhà nước",
          "thành phố",
          "bác sĩ",
          "kỹ sư",
          "giáo viên",
          "học sinh",
          "sinh viên",
          "công nhân",
          "nông thôn",
          "đô thị",
          "quân đội",
          "công an",
          "y tế",
          "giáo dục",
          "văn hóa"
        ])
analysis_settings.filter_component.add_filter(vi_dictionary_decompounder)


analysis_settings.tokenizer_component.add_tokenizer(vi_ngram_tokenizer)

analyzer = AnalyzerCustom(name="analyzer-vi-ngram")
analyzer.set_tokenizer(vi_ngram_tokenizer)
analyzer.add_filter(vi_stopwords)
analyzer.add_filter(Filter(type="lowercase"))
analyzer.add_filter(Filter(type="asciifolding"))
analyzer.add_filter(vi_dictionary_decompounder)

analysis_settings.analyzer_component.add_analyzer(analyzer)

print(analysis_settings.build())

json.dump(analysis_settings.build(), open('sample_analysis.json', 'w', encoding='utf-8'), indent=4)


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
            "analysis":{
                "filter": {
                    "vi_stopwords": {
                        "type": "stop",
                        "stopwords": words
                    }
                },
                "analyzer": {
                    "analyzer-vietnamese": {
                      "tokenizer": "standard",
                      "filter": [
                        "vi_stopwords"
                      ]
                    }
                  }
            }
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
json.dump(index_template, open('index_template.json', 'w', encoding='utf-8'), indent=4)


if client.indices.exists_index_template(name="baolaodong_template"):
    client.indices.delete_index_template(name="baolaodong_template")

client.indices.put_index_template(
    name="baolaodong_template",
    index_patterns=index_template['index_patterns'],
    template=index_template['template']
)


