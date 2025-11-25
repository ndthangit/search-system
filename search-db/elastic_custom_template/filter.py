import json
from typing import Literal, List


# --- Định nghĩa các class cho Filter ---

class Filter:
    """Lớp cơ sở cho tất cả các loại filter."""

    def __init__(self, type: Literal["stop", "stemmer", "unique", "synonym", "length","asciifolding","lowercase","dictionary_decompounder"]):
        self.type = type
        self.name = type



class FilterCustom(Filter):
    def __init__(self, name: str, type: Literal["stop", "stemmer", "unique", "synonym", "length", "asciifolding","dictionary_decompounder"]):
        super().__init__(type=type)
        self.name = name

class FilterStop(FilterCustom):
    def __init__(self, name: str, stopwords: List[str]):
        super().__init__(name=name, type="stop")
        self.stopwords = stopwords

class FilterDictionaryDecompounder(FilterCustom):
    def __init__(self, name: str, word_list: list[str]):
        super().__init__(name=name, type="dictionary_decompounder")
        self.word_list = word_list



class FilterComponent:
    """Lớp quản lý và xây dựng từ điển 'filter'."""

    def __init__(self):
        self.filters: List[Filter] = []

    def add_filter(self, filter_instance: Filter):
        """Thêm một instance filter vào component."""
        self.filters.append(filter_instance)

    def build(self) -> dict:
        """Xây dựng từ điển 'filter' cuối cùng."""
        filter_dict = {}
        for f in self.filters:
            # Tạo entry cơ bản
            if isinstance(f, FilterCustom):
                config = {"type": f.type}

                # Thêm các thuộc tính cụ thể cho từng loại
                if f.type == "stop":
                    config["stopwords"] = getattr(f, 'stopwords', [])
                elif f.type == "dictionary_decompounder":
                    config["word_list"] = getattr(f, 'word_list', [])

                # FilterUnique không cần thuộc tính gì thêm

                filter_dict[getattr(f, 'name', f.type)] = config

        return filter_dict


# --- Mẫu chạy thử (Dựa trên file filter.py của bạn) ---

# 1. Giả lập việc đọc file stop_word.txt
# (Trong thực tế, bạn sẽ bỏ comment phần đọc file ở đây)
# with open('../data/stop_word.txt', 'r', encoding='utf-8') as file:
#     words = [line.strip() for line in file if line.strip()]
# words = ["và", "là", "của", "trên", "tôi", "bạn"]  # Dùng list giả lập
#
# # 2. Tạo các instance filter cụ thể
# vi_stopwords = FilterStop(name="vi_stopwords", stopwords=words)
# vi_stemmer = FilterStemmer(name="vi_stemmer", language="minimal_english")
# vi_remove_duplicates = FilterUnique(name="vi_remove_duplicates")
#
# # 3. Tạo FilterComponent
# filter_component = FilterComponent()
#
# # 4. Thêm các filter vào component
# filter_component.add_filter(vi_stopwords)
# filter_component.add_filter(vi_stemmer)
# filter_component.add_filter(vi_remove_duplicates)
#
# # 5. Build từ điển cuối cùng
# built_filters = filter_component.build()
#
# # 6. Tạo lại cấu trúc template đầy đủ
# final_template = {
#     "template": {
#         "settings": {
#             "analysis": {
#                 # Đặt kết quả build vào đúng vị trí
#                 "filter": built_filters
#             }
#         }
#     }
# }
#
# # 7. In kết quả ra để so sánh
# print(json.dumps(final_template, indent=4, ensure_ascii=False))