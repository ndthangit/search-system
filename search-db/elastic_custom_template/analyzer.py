from typing import List, Union

from elastic_custom_template.char_filter import CharFilter
from elastic_custom_template.filter import Filter
from elastic_custom_template.tokenizer import Tokenizer


# --- Định nghĩa các class cho Analyzer ---

class Analyzer:
    """Lớp cơ sở cho tất cả các loại analyzer."""

    def __init__(self, type: str):
        self.name = ""
        self.type = type

    def build(self) -> dict:
        """Phương thức trừu tượng cần được triển khai bởi lớp con."""
        raise NotImplementedError("Subclasses must implement build() method")


class AnalyzerCustom(Analyzer):
    """
    Định nghĩa cho 'custom' analyzer, đã được tối ưu.

    Sử dụng 'builder pattern' (phương thức trả về self)
    để dễ dàng 'chain' (nối) các lệnh.
    """

    def __init__(self,
                 name: str,
                 tokenizer: Tokenizer = None,
                 char_filters: List[Union[CharFilter, str]] = None,
                 filters: List[Union[Filter, str]] = None):
        # 1. Loại bỏ tham số 'name' không được sử dụng
        super().__init__(type="custom")

        self.name = name
        self.tokenizer = tokenizer
        self.char_filters = char_filters or []
        self.filters = filters or []

    def set_tokenizer(self, tokenizer: Tokenizer):
        """Gán (hoặc ghi đè) tokenizer."""
        self.tokenizer = tokenizer
        return self  # 3. Trả về 'self' để cho phép 'chaining'

    def add_char_filter(self, char_filter: Union[CharFilter, str]):
        """
        Thêm MỘT char_filter vào danh sách.
        Đổi tên từ 'add_char_filters' (số nhiều) thành 'add_char_filter' (số ít)
        để phản ánh đúng hành vi.
        """
        self.char_filters.append(char_filter)
        return self

    def add_filter(self, new_filter: Union[Filter, str]):
        """
        Thêm MỘT filter vào danh sách.

        SỬA LỖI: self.filters.append(new_filter) thay vì self.filters.append(Filter).
        ĐỔI TÊN: Đổi tên tham số 'filter' thành 'new_filter' để tránh
                 trùng lặp với hàm 'filter' built-in của Python.
        """
        # 4. SỬA LỖI quan trọng: Dùng biến 'new_filter', không phải class 'Filter'
        self.filters.append(new_filter)
        return self

    def build(self):
        """Xây dựng và trả về từ điển cấu hình analyzer."""
        config = {self.name: {
                "type": self.type,
                "tokenizer": self.tokenizer.name if self.tokenizer else None,
                "char_filter": [cf.name if isinstance(cf, CharFilter) else cf for cf in self.char_filters],
                "filter": [f.name if isinstance(f, Filter) else f for f in self.filters]
            }
        }

        return {k: v for k, v in config.items() if v}

class AnalyzerComponent:
    """Lớp quản lý và xây dựng từ điển 'analyzer'."""

    def __init__(self):
        self.analyzers: List[Analyzer] = []

    def add_analyzer(self, analyzer_instance: Analyzer):
        """Thêm một instance analyzer vào component."""
        self.analyzers.append(analyzer_instance)

    def build(self) -> dict:
        """Xây dựng từ điển 'analyzer' cuối cùng."""
        analyzer_dict = {}
        for a in self.analyzers:
            # Sử dụng phương thức build() của từng analyzer để lấy cấu hình
            analyzer_dict.update(a.build())
        return analyzer_dict


# --- Mẫu chạy thử (Dựa trên JSON của bạn) ---

# 1. Tạo analyzer "nfd_normalized"
#    (Loại custom này không có "type": "custom" tường minh)
# nfd_analyzer = AnalyzerCustom(
#     name="nfd_normalized",
#     tokenizer="icu_tokenizer"
# )
# nfd_analyzer.add_char_filters(["nfd_normalizer"])
# # Không gọi set_explicit_type()
#
# # 2. Tạo analyzer "vi_ngram_analyzer"
# #    (Loại custom này CÓ "type": "custom" tường minh)
# vi_ngram_analyzer = AnalyzerCustom(
#     name="vi_ngram_analyzer",
#     tokenizer="vi_ngram_tokenizer"
# )
# vi_ngram_analyzer.add_filters(["lowercase", "asciifolding"])
# vi_ngram_analyzer.set_explicit_type()  # Đánh dấu để thêm type
#
# # 3. Tạo AnalyzerComponent
# analyzer_component = AnalyzerComponent()
#
# # 4. Thêm các analyzer vào component
# analyzer_component.add_analyzer(nfd_analyzer)
# analyzer_component.add_analyzer(vi_ngram_analyzer)
#
# # 5. Build từ điển cuối cùng
# built_analyzers = analyzer_component.build()
#
# # 6. Tạo lại cấu trúc "analysis" (chỉ chứa phần analyzer)
# final_analysis_section = {
#     "analysis": {
#         "analyzer": built_analyzers
#         # Lưu ý: Các phần khác như char_filter, filter sẽ được
#         # build bởi các component tương ứng của chúng
#     }
# }
#
# # 7. In kết quả ra để so sánh
# print(json.dumps(final_analysis_section, indent=4, ensure_ascii=False))