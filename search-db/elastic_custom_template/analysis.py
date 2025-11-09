import json

from elastic_custom_template.analyzer import AnalyzerComponent, Analyzer, AnalyzerCustom
from elastic_custom_template.char_filter import CharFilterComponent, CharFilter, CharFilterMapping
from elastic_custom_template.filter import FilterComponent, Filter, FilterStop
from elastic_custom_template.tokenizer import TokenizerComponent, Tokenizer, TokenizerNgram


class AnalysisComponent:
    """
    Lớp tổng hợp để quản lý analyzers, filters, tokenizers, và char_filters
    và xây dựng 'analysis' JSON cuối cùng.
    """

    def __init__(self):
        # Khởi tạo các component con từ các file
        self.char_filter_component = CharFilterComponent()
        self.filter_component = FilterComponent()
        self.tokenizer_component = TokenizerComponent()
        self.analyzer_component = AnalyzerComponent()

    # --- Các phương thức 'add' để ủy quyền (delegation) ---

    def add_char_filter(self, char_filter: CharFilter):
        """Thêm một char_filter vào component con."""
        self.char_filter_component.add_char_filter(char_filter)

    def add_filter(self, filter_instance: Filter):
        """Thêm một filter vào component con."""
        self.filter_component.add_filter(filter_instance)

    def add_tokenizer(self, tokenizer_instance: Tokenizer):
        """Thêm một tokenizer vào component con."""
        self.tokenizer_component.add_tokenizer(tokenizer_instance)

    def add_analyzer(self, analyzer_instance: Analyzer):
        """Thêm một analyzer vào component con."""
        self.analyzer_component.add_analyzer(analyzer_instance)

    # --- Phương thức Build chính ---

    def build(self) -> dict:
        """Xây dựng đối tượng 'analysis' hoàn chỉnh."""
        analysis_data = {}

        # Build từng phần
        built_char_filters = self.char_filter_component.build()
        built_filters = self.filter_component.build()
        built_tokenizers = self.tokenizer_component.build()
        built_analyzers = self.analyzer_component.build()

        # Chỉ thêm vào 'analysis' nếu chúng không rỗng
        if built_char_filters:
            analysis_data["char_filter"] = built_char_filters
        if built_filters:
            analysis_data["filter"] = built_filters
        if built_tokenizers:
            analysis_data["tokenizer"] = built_tokenizers
        if built_analyzers:
            analysis_data["analyzer"] = built_analyzers

        # Trả về cấu trúc cuối cùng
        if analysis_data:
            return {"analysis": analysis_data}
        return {}

# --- 1. Tạo builder tổng ---
analysis_builder = AnalysisComponent()

# --- 2. Thêm Char Filter ---
vi_char_filter = CharFilterMapping(name="vi_char_filter")
vi_char_filter.add_mapping("đ => d")
vi_char_filter.add_mapping("Đ => D")
analysis_builder.add_char_filter(vi_char_filter)

# --- 3. Thêm Filter ---
stop_words = ["và", "là", "của"]
vi_stopwords = FilterStop(name="vi_stopwords", stopwords=stop_words)
analysis_builder.add_filter(vi_stopwords)

# Thêm một filter dùng built-in stopwords
english_stop = FilterStop(name="english_stop", stopwords="_english_")
analysis_builder.add_filter(english_stop)

# --- 4. Thêm Tokenizer ---
vi_tokenizer = TokenizerNgram(
    name="vi_ngram_tokenizer",
    min_gram=2,
    max_gram=3,
    token_chars=["letter", "digit"]
)
analysis_builder.add_tokenizer(vi_tokenizer)

# --- 5. Thêm Analyzer (sử dụng các tên ở trên) ---
vi_analyzer = AnalyzerCustom(
    name="vietnamese_analyzer",
    tokenizer="vi_ngram_tokenizer"  # Sử dụng tokenizer ở trên
)
vi_analyzer.add_char_filters(["vi_char_filter"]) # Sử dụng char_filter ở trên
vi_analyzer.add_filters(["lowercase", "asciifolding", "vi_stopwords"]) # Sử dụng filter ở trên
vi_analyzer.set_explicit_type() # Đặt "type": "custom"
analysis_builder.add_analyzer(vi_analyzer)

# --- 6. Build và In kết quả ---
final_analysis_settings = analysis_builder.build()
print(json.dumps(final_analysis_settings, indent=4, ensure_ascii=False))