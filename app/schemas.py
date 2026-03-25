from pydantic import BaseModel

class SummaryRequest(BaseModel):
    text: str
    max_length: int = 128
    min_length: int = 30
    do_sample: bool = False

class SummaryResponse(BaseModel):
    summary: str