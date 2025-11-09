import json
from typing import Literal

# --- (Dán các class bạn đã cung cấp vào đây) ---
class CharFilter:
    def __init__(self, type: Literal["mapping", "pattern_replace"]):
        self.name = ""
        self.type = type

class CharFilterMapping(CharFilter):
    def __init__(self, name: str):
        super().__init__(type="mapping")
        self.name = name
        self.mappings = []

    def add_mapping(self, mapping: str):
        mapping = mapping.strip()
        # Một kiểm tra đơn giản, có thể cải thiện thêm
        if "=>" not in mapping:
            raise ValueError("Mapping must be in the format 'a => b'")
        self.mappings.append(mapping)


class CharFilterPattern(CharFilter):
    def __init__(self, name: str, pattern: str, replacement: str):
        super().__init__(type="pattern_replace")
        self.name = name
        self.pattern = pattern
        self.replacement = replacement


class CharFilterComponent:
    def __init__(self):
        self.char_filters = []

    def add_char_filter(self, char_filter: CharFilter):
        self.char_filters.append(char_filter)

    def build(self):
        char_filter_dict = {}
        for char_filter in self.char_filters:
            if char_filter.type == "mapping":
                char_filter_dict[char_filter.name] = {
                    "type": "mapping",
                    "mappings": char_filter.mappings
                }
            elif char_filter.type == "pattern_replace":
                char_filter_dict[char_filter.name] = {
                    "type": "pattern_replace",
                    "pattern": char_filter.pattern,
                    "replacement": char_filter.replacement
                }
        return char_filter_dict

# --- Mẫu chạy thử ---

# 1. Tạo một instance của CharFilterMapping
# Tên "vi_char_filter" được lấy từ JSON
# vi_char_filter = CharFilterMapping(name="vi_char_filter")
#
# # 2. Thêm tất cả các mapping từ JSON vào instance
# mappings_list = [
#     "đ => d",
#     "Đ => D",
#     "òa => oà",
#     "óa => oá",
#     "ỏa => oả",
#     "õa => oã",
#     "ọa => oạ"
# ]
#
# for mapping in mappings_list:
#     vi_char_filter.add_mapping(mapping)
#
# # 3. Tạo CharFilterComponent để quản lý các filter
# char_filter_component = CharFilterComponent()
#
# # 4. Thêm filter vừa tạo vào component
# char_filter_component.add_char_filter(vi_char_filter)
#
# # (Bạn cũng có thể thêm một CharFilterPattern nếu muốn)
# pattern_example = CharFilterPattern(name="remove_dots", pattern="\\.", replacement="")
# char_filter_component.add_char_filter(pattern_example)
#
# # 5. Build từ điển cuối cùng
# built_char_filters = char_filter_component.build()
#
# # 6. Tạo lại cấu trúc template đầy đủ
# final_template = {
#     "template": {
#         "settings": {
#             "analysis": {
#                 # Đặt kết quả build vào đúng vị trí
#                 "char_filter": built_char_filters
#             }
#         }
#     }
# }
#
# # 7. In kết quả ra để so sánh
# print(json.dumps(final_template, indent=4, ensure_ascii=False))





