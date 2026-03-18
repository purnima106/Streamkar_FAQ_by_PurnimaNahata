from pydantic import BaseModel

class FAQRequest(BaseModel):
    question: str
    answer: str

class QueryRequest(BaseModel):
    query: str
