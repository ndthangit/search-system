import ast
import re
from datetime import datetime

import pandas as pd
from elasticsearch import helpers
import traceback
from setup import client

data = pd.read_json("data/data.json")

data.head()

# Process NDJSON files

# Create index (matches wikipedia-people* pattern)

INDEX_NAME = "articles-json"
if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME)
    print(f"Index '{INDEX_NAME}' created successfully")
else:
    client.indices.delete(index=INDEX_NAME)
#
batch_size = 5
actions = []


count =0
for index, row in data.iterrows():

    if count >10:
        break

    count +=1

    # Prepare ES document
    es_doc = {
        "_index": INDEX_NAME,
        "_id": row['link'],
        "_source": {
            "link": row['link'],
            "title-va": row['title'],
            "title-vska": row['title'],
            "summary-va": row['summary'],
            "summary-vska": row['summary']

        }
    }
    # print(actions)
    actions.append(es_doc)

    # Bulk index when batch is full
    if len(actions) >= batch_size:
        # try:

            helpers.bulk(client, actions)
            # print(f"Indexed {len(actions)} documents from {file_names[5]}")

            actions = []


        # except Exception as e:
        #     print(f"Error indexing batch: {e}")
        #     print(actions)

# Index any remaining documents
# if actions:
#     try:
#         helpers.bulk(client, actions)
#         print(f"Indexed final {len(actions)} documents")
#     except Exception as e:
#         print(f"Error indexing final batch: {e}")
#         print(actions)

print("Ingestion complete!")
