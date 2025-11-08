import json
from typing import Literal, List


# --- Định nghĩa các class cho Tokenizer ---

class Tokenizer:
    """Lớp cơ sở cho tất cả các loại tokenizer."""

    def __init__(self, type: Literal["ngram", "standard", "pattern", "path_hierarchy"]):
        # Mở rộng Literal để bao gồm các loại phổ biến khác
        self.name = ""
        self.type = type


class TokenizerNgram(Tokenizer):
    """Định nghĩa cho 'ngram' tokenizer."""

    def __init__(self, name: str, min_gram: int, max_gram: int, token_chars: List[str]):
        super().__init__(type="ngram")
        self.name = name
        self.min_gram = min_gram
        self.max_gram = max_gram
        self.token_chars = token_chars


# Bạn có thể thêm các class Tokenizer khác ở đây (ví dụ: TokenizerPattern)
# class TokenizerPattern(Tokenizer):
#     def __init__(self, name: str, pattern: str):
#         super().__init__(type="pattern")
#         self.name = name
#         self.pattern = pattern

class TokenizerComponent:
    """Lớp quản lý và xây dựng từ điển 'tokenizer'."""

    def __init__(self):
        self.tokenizers: List[Tokenizer] = []

    def add_tokenizer(self, tokenizer_instance: Tokenizer):
        """Thêm một instance tokenizer vào component."""
        self.tokenizers.append(tokenizer_instance)

    def build(self) -> dict:
        """Xây dựng từ điển 'tokenizer' cuối cùng."""
        tokenizer_dict = {}
        for t in self.tokenizers:
            # Tạo entry cơ bản
            config = {"type": t.type}

            # Thêm các thuộc tính cụ thể cho từng loại
            if t.type == "ngram":
                config["min_gram"] = getattr(t, 'min_gram')
                config["max_gram"] = getattr(t, 'max_gram')
                config["token_chars"] = getattr(t, 'token_chars')
            # elif t.type == "pattern":
            #     config["pattern"] = getattr(t, 'pattern')

            tokenizer_dict[t.name] = config

        return tokenizer_dict


# --- Mẫu chạy thử (Dựa trên file tokenizer.py của bạn) ---

# 1. Tạo instance tokenizer cụ thể
vi_syllable_tokenizer = TokenizerNgram(
    name="vi_syllable_tokenizer",
    min_gram=2,
    max_gram=3,
    token_chars=["letter", "digit"]
)

# 2. Tạo TokenizerComponent
tokenizer_component = TokenizerComponent()

# 3. Thêm tokenizer vào component
tokenizer_component.add_tokenizer(vi_syllable_tokenizer)

# 4. Build từ điển cuối cùng
built_tokenizers = tokenizer_component.build()

# 5. Tạo lại cấu trúc template đầy đủ
final_template = {
    "template": {
        "settings": {
            "analysis": {
                # Đặt kết quả build vào đúng vị trí
                "tokenizer": built_tokenizers
            }
        }
    }
}

# 6. In kết quả ra để so sánh
print(json.dumps(final_template, indent=4, ensure_ascii=False))