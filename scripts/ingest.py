import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app.services.embedding import get_embedding
from app.db.vector_store import add_faq, create_collection

# Ensure the collection exists locally before we add FAQs
create_collection()

with open("data/faqs.json", "r") as f:
    faqs = json.load(f)

for faq in faqs:
    emb = get_embedding(faq["question"])
    add_faq(faq["question"], faq["answer"], emb)

print("Data ingested successfully!")
