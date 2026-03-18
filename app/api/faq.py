from fastapi import APIRouter
from app.models.schemas import FAQRequest
from app.services.embedding import get_embedding
from app.db.vector_store import add_faq

router = APIRouter()

@router.post("/add_faq")
def add_faq_api(data: FAQRequest):
    embedding = get_embedding(data.question)
    add_faq(data.question, data.answer, embedding)
    return {"status": "FAQ added"}

@router.post("/bulk_upload")
def bulk_upload(faqs: list[FAQRequest]):
    for faq in faqs:
        emb = get_embedding(faq.question)
        add_faq(faq.question, faq.answer, emb)

    return {"status": "Bulk upload complete"}
