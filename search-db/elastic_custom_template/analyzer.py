import json
from typing import Literal, List, Optional


# --- Định nghĩa các class cho Analyzer ---

class Analyzer:
    """Lớp cơ sở cho tất cả các loại analyzer."""

    def __init__(self, type: str):
        self.name = ""
        self.type = type


class AnalyzerCustom(Analyzer):
    """Định nghĩa cho 'custom' analyzer."""

    def __init__(self, name: str, tokenizer: str):
        super().__init__(type="custom")
        self.name = name
        self.tokenizer = tokenizer
        self.char_filters: List[str] = []
        self.filters: List[str] = []
        # Cờ để quyết định có thêm "type": "custom" vào JSON hay không
        self.explicit_type = False

    def add_char_filters(self, char_filter_names: List[str]):
        """Thêm một danh sách tên char_filter."""
        self.char_filters.extend(char_filter_names)

    def add_filters(self, filter_names: List[str]):
        """Thêm một danh sách tên filter."""
        self.filters.extend(filter_names)

    def set_explicit_type(self):
        """Đánh dấu để thêm 'type: "custom"' khi build."""
        self.explicit_type = True


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
            if a.type == "custom":
                # Đảm bảo đây là instance AnalyzerCustom
                if not isinstance(a, AnalyzerCustom):
                    continue

                config = {
                    "tokenizer": a.tokenizer
                }

                # Chỉ thêm "type": "custom" nếu được đánh dấu
                if a.explicit_type:
                    config["type"] = "custom"

                # Chỉ thêm các trường nếu chúng không rỗng
                if a.char_filters:
                    config["char_filter"] = a.char_filters

                if a.filters:
                    config["filter"] = a.filters

                analyzer_dict[a.name] = config

            # (Bạn có thể thêm logic cho các loại analyzer khác ở đây)

        return analyzer_dict


# --- Mẫu chạy thử (Dựa trên JSON của bạn) ---

# 1. Tạo analyzer "nfd_normalized"
#    (Loại custom này không có "type": "custom" tường minh)
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

# 6. Tạo lại cấu trúc "analysis" (chỉ chứa phần analyzer)
final_analysis_section = {
    "analysis": {
        "analyzer": built_analyzers
        # Lưu ý: Các phần khác như char_filter, filter sẽ được
        # build bởi các component tương ứng của chúng
    }
}

# 7. In kết quả ra để so sánh
print(json.dumps(final_analysis_section, indent=4, ensure_ascii=False))