import json
import os
from elasticsearch import Elasticsearch
from elastic_custom_template.filter import FilterStop

client = Elasticsearch(
    hosts=[os.getenv('ELASTICSEARCH_HOST', 'http://localhost:9200')],
    basic_auth=(
        os.getenv('ELASTICSEARCH_USERNAME', 'elastic'),
        os.getenv('ELASTIC_PASSWORD', 'elastic'),
    ),
    verify_certs=False,
    ssl_show_warn=False
)
client.info()


# --- Tạo filter stopwords từ file ---

with open('data/stop_word.txt', 'r', encoding='utf-8') as file:
    words = [line.strip() for line in file if line.strip()]
print(words)
# # 2. Tạo các instance filter cụ thể
vi_stopwords = FilterStop(name="vi_stopwords", stopwords=words)

import pandas as pd

df = pd.read_csv("hf://datasets/tsdocode/vietnamese-dictionary/vi_dictionary.csv")

print(df.columns)


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

            "similarity": {
                "title_bm25": {
                    "type": "BM25",
                    "b": 0.3,    # Tiêu đề thường ngắn nên b nhỏ
                    "k1": 1.5    # Tăng trọng số cho tiêu đề
                },
                "content_bm25": {
                    "type": "BM25",
                    "b": 0.75,
                    "k1": 1.2
                }
            },

            "analysis":{
                "filter": {
                    "vi_stopwords": {
                        "type": "stop",
                        "stopwords": words
                    },
                    "vn_number_mapper": {
                        "type": "pattern_replace",
                        "pattern": "(\\d+) (\\d+)",
                        "replacement": "$1-$2"
                      },
                    "my_synonym_filter": {
                      "type": "synonym_graph",
                      "synonyms": [
                        # Thể thao chung
                        "thể thao, sport, thể dục",
                        "vận động viên, vđv, cầu thủ, siêu sao",
                        "trận đấu, trận, cuộc đọ sức, thi đấu",
                         # Bóng đá

                        "đá bóng, bóng đá, túc cầu",
                        "sân vận động, sân cỏ, svd",
                        "huấn luyện viên, hlv",
                        "trọng tài, vua áo đen",
                        "vô địch, quán quân",
                         # Các môn khác
                        "bơi lội, bơi",
                        "thể hình, gym",
                        "điền kinh, chạy bộ"
                      ]
                    },
                    "number_synonym_filter": {
                        "type": "synonym",
                        "synonyms": [
                            "không => 0",
                            "một, mốt => 1",
                            "hai => 2",
                            "ba => 3",
                            "bốn, tư => 4",
                            "năm, lăm, nhăm => 5",
                            "sáu => 6",
                            "bảy => 7",
                            "tám => 8",
                            "chín => 9",
                            "mười, mươi, chục => 0"
                        ]
                    },

                    "my_shingle_filter": {
                      "type": "shingle",
                      "min_shingle_size": 2,
                      "max_shingle_size": 4,
                      "output_unigrams": "true"
                    },
                    "keep_words_filter": {
                        "type": "keep",
                        "keep_words": df['word'].dropna().tolist()
                    }
                },

                "analyzer": {
                    "vietnamese_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "number_synonym_filter",
                            "vn_number_mapper",
                            "vi_stopwords",
                            "asciifolding",
                            "my_shingle_filter",
                        ]

                    },
                    "vietnamese_search_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "number_synonym_filter",
                            "vn_number_mapper",
                            "vi_stopwords",
                            "my_synonym_filter",
                            "asciifolding"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "link": {
                    "type": "keyword"
                },
                "title-va": {
                    "analyzer": "vietnamese_analyzer",
                    "search_analyzer": "vietnamese_search_analyzer",
                    "similarity": "title_bm25",
                    "type": "text"
                },

                "content-va": {
                    "analyzer": "vietnamese_analyzer",
                    "search_analyzer": "vietnamese_search_analyzer",
                    "similarity": "content_bm25",
                    "type": "text"
                },

                "pub_ts":{
                    "type": "date"
                },
                "last_updated": {
                    "type": "date"
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
