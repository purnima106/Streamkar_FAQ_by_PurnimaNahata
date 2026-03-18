from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

from app.core.config import COLLECTION_NAME

# Use persistent local storage instead of Docker
client = QdrantClient(path="local_qdrant")

def create_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

def add_faq(question, answer, embedding):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"question": question, "answer": answer},
            )
        ],
    )

def search(query_embedding, limit=5):
    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit,
    )
