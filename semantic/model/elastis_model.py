from pydantic import BaseModel
from typing import List
class Document(BaseModel):
    name: str
    abstract: str
    url: str

class SearchResponse(BaseModel):
    success: bool
    list_docs: List[Document]

class SearchRequest(BaseModel):
    text: str