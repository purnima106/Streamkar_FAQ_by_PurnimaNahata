import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app.services.embedding import get_embedding
from app.db.vector_store import add_faq, create_collection

# Step 1: Ensure collection exists
create_collection()

# Step 2: Load data
with open("data/faqs.json", "r") as f:
    faqs = json.load(f)

# Step 3: Insert data
for faq in faqs:
    emb = get_embedding(faq["question"])

    print("Embedding size:", len(emb))  # ✅ debug

    add_faq(faq["question"], faq["answer"], emb)

print("✅ Data ingested successfully!")