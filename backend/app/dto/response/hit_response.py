from pydantic import BaseModel
from typing import List, Any
import math
from app.dto.response.document_dto import DocumentDto

class HitResponse(BaseModel):
    index: str
    id: str  
    score: float | None = None
    source: DocumentDto