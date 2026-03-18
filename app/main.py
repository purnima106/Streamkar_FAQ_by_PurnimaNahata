from fastapi import FastAPI
from app.api import faq, query
from app.db.vector_store import create_collection

app = FastAPI()

@app.on_event("startup")
def startup():
    create_collection()

@app.get("/")
def root():
    return {"message": "StreamKar FAQ Bot is running 🚀"}

app.include_router(faq.router)
app.include_router(query.router)
