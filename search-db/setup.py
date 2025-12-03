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
                    },
                    "vn_number_mapper": {
                        "type": "pattern_replace",
                        "pattern": "(\\d+)_(\\d+)",
                        "replacement": "$1$2"
                      },
                    "synonym_sports": {
                      "type": "synonym",
                      "synonyms": [
                        "bóng đá => thể thao bóng đá, bóng đá sân cỏ, bóng đá chuyên nghiệp, đá bóng, thi đấu bóng, chơi bóng",
                        "thể thao => vận động, động lực thể chất, kỹ năng thể chất, kỹ năng thể thao, thể thao chuyên nghiệp, năng động, chuyên nghiệp, sức mạnh",
                        "thi đấu => tham gia thi đấu, đấu tranh, đấu cuộc, trận đấu, cuộc thi, giải đấu, cạnh tranh, quyết liệt, nhiệt huyết, trận thi"
                      ],
                      "expand": "true"
                    },
                },
                "char_filter": {
                  "number_mapping": {
                    "type": "mapping",
                    "mappings": [
                      "không => 0",
                      "một => 1",
                      "mốt => 1",
                      "hai => 2",
                      "ba => 3",
                      "bốn => 4",
                      "tư => 4",
                      "năm => 5",
                      "lăm => 5",
                      "nhăm => 5",
                      "sáu => 6",
                      "bảy => 7",
                      "tám => 8",
                      "chín => 9",
                      "mười => _10",
                      "chục => _10",
                      "trăm => _100",
                      "nghìn => _1000",
                      "ngàn => _1000",
                      "vạn => _10000",
                      "triệu => _1000000",
                      "tỉ => _1000000000",
                      "lẻ => .",
                      "linh => ."

                    ]
                  }
                },
                "analyzer": {
                    "analyzer-vietnamese": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "vi_stopwords",
                            "lowercase",
                            "asciifolding",
                            "vn_number_mapper",
                            "synonym_sports"
                        ],
                        "char_filter": [
                            "number_mapping"
                        ]
                    }
                  }

            }
        },
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text"},
                "summary": {"type": "text"}
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


