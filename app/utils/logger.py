import logging
import os

os.makedirs("app/logs", exist_ok=True)

logging.basicConfig(
    filename="app/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_query(query, answer):
    logging.info(f"QUERY: {query} | ANSWER: {answer}")
