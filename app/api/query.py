from fastapi import APIRouter
from app.models.schemas import QueryRequest
from app.services.embedding import get_embedding
from app.services.retriever import retrieve_context
from app.services.llm import generate_answer
from app.utils.logger import log_query

router = APIRouter()

@router.post("/ask")
def ask_question(data: QueryRequest):
    embedding = get_embedding(data.query)

    context, score = retrieve_context(embedding)

    print("Retrieved Context:\n", context)
    print("Score:", score)

    if score < 0.5:
        return {"answer": "I don't have enough information to answer that."}

    answer = generate_answer(context, data.query)

    log_query(data.query, answer)

    return {"answer": answer}

