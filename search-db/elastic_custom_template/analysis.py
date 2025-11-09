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

