from typing import List, Optional
from pydantic import BaseModel

class MultiMatchSearchRequest(BaseModel):
    query: str                  # từ khóa tìm kiếm
    fields: List[str]           # list các field để multi_match
    page: Optional[int] = 1    # index bắt đầu (offset)
    size: Optional[int] = 10    # số document trả về
