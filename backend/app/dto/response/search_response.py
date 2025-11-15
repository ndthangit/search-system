from pydantic import BaseModel
from typing import List, Any
import math

class SearchResponse(BaseModel):
    pageNumber: int
    pageSize: int
    totalElements: int
    totalPages: int
    data: List[Any]
