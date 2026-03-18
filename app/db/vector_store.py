from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

from app.core.config import COLLECTION_NAME

client = QdrantClient(path="local_qdrant")


def create_collection():
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")


def add_faq(question, answer, embedding):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "question": question,
                    "answer": answer
                },
            )
        ],
    )
    print("Inserted:", question)


def search(query_embedding):
    results = client.query_points(
        collection_name=COLLECTION_NAME,  # ✅ FIXED
        query=query_embedding,
        limit=3
    )

    print("RAW SEARCH:", results)

    return results.points