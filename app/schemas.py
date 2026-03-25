from pydantic import BaseModel
from typing import List

# 분류 Request/Response (Spring과 100% 호환)
class CategoryRequest(BaseModel):
    url: str
    text: str
    categories: List[int]

class CategoryResponse(BaseModel):
    categoryId: int
    keywords: str

# 요약 Request/Response
class SummaryRequest(BaseModel):
    text: str
    max_length: int = 128
    min_length: int = 30
    do_sample: bool = False

class SummaryResponse(BaseModel):
    summary: str