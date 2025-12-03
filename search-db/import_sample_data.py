import ast
import re
from datetime import datetime

import pandas as pd
from elasticsearch import helpers
import traceback
from setup import client


def safe_literal_eval(val):
    """Chuyển đổi string list thành Python list an toàn"""
    if pd.isna(val) or val == '':
        return []
    try:
        # Xử lý trường hợp có dấu ngoặc vuông
        if val.startswith('[') and val.endswith(']'):
            return ast.literal_eval(val)
        else:
            # Nếu không phải list, coi như single value
            return [val.strip()]
    except (ValueError, SyntaxError):
        # Nếu có lỗi, split bằng dấu phẩy
        return [item.strip().strip("'\"") for item in val.split(',')]

def convert_vietnamese_date(date_str):
    """Chuyển đổi date tiếng Việt sang định dạng ISO"""
    if not date_str:
        return None

    try:
        # Loại bỏ các phần thừa như "Thứ sáu,", "(GMT+7)"
        cleaned = re.sub(r'Thứ\s+\w+,\s*', '', date_str)  # Bỏ "Thứ sáu, "
        cleaned = re.sub(r'\s*\(GMT[+-]\d+\)', '', cleaned)  # Bỏ "(GMT+7)"
        cleaned = cleaned.strip()

        # Parse thành datetime object
        dt = datetime.strptime(cleaned, '%d/%m/%Y %H:%M')

        # Chuyển sang ISO format
        return dt.isoformat()

    except Exception as e:
        print(f"Lỗi convert date: {date_str} - {e}")
        return None

data = pd.read_csv("data/Dataset_articles_NoID.csv")


# Process NDJSON files

# Create index (matches wikipedia-people* pattern)

INDEX_NAME = "articles-csv"
if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME)
    print(f"Index '{INDEX_NAME}' created successfully")
else:
    client.indices.delete(index=INDEX_NAME)

batch_size = 5
actions = []


count =0
for index, row in data.iterrows():

    # Xử lý tags từ string list thành Python list
    tags = safe_literal_eval(row['Tags'])

    # Xử lý authors tương tự
    authors = safe_literal_eval(row['Author(s)'])


    # Sử dụng giá trị mặc định nếu thiếu
    # if not full_text or not full_text.strip():
    #     full_text = "No content available"

    if count >10:
        break

    count +=1

    # Prepare ES document
    es_doc = {
        "_index": INDEX_NAME,
        "_id": row['URL'],
        "_source": {
            "url": row['URL'],
            "title": row['Title'],
            "summary": row['Summary'],
            "contents": row['Contents'],
            "date": convert_vietnamese_date(row['Date']),
            "authors": authors,
            "category": row['Category'],
            "tags": tags
        }
    }
    print(actions)
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
