from pydantic import BaseModel
from typing import List, Any
import math
from app.dto.response.hit_response import HitResponse

class SearchResponse(BaseModel):
    pageNumber: int
    pageSize: int
    totalElements: int
    totalPages: int
    took: int | None = None
    maxScore: float | None = None
    data: List[HitResponse]
