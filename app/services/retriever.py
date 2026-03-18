from app.db.vector_store import search

def retrieve_context(query_embedding):
    results = search(query_embedding)

    context = ""
    max_score = 0

    for r in results:
        score = r.score
        max_score = max(max_score, score)

        q = r.payload["question"]
        a = r.payload["answer"]
        context += f"""
FAQ:
Question: {q}
Answer: {a}
"""

    return context, max_score
