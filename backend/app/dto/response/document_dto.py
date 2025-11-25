from pydantic import BaseModel
from typing import List, Any
import math

class DocumentDto(BaseModel):
    url: str   
    title: str
    summary: str
    contents: str
    date: str           # ISO8601
    authors: List[str]
    category: str
    tags: List[str]
