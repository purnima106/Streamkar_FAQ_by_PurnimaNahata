from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = None
tokenizer = None

def load_model():
    global model, tokenizer

    if model is None:
        model_name = "Qwen/Qwen2.5-3B-Instruct"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

#type of prompt:-Instruction + Context (RAG Prompting) for streamkar

def generate_answer(context, query):
    load_model()  # load only once

    prompt = f"""
You are a highly accurate FAQ assistant for StreamKar.

Your job is to answer user questions ONLY using the provided context.

---------------------
RULES:
1. ONLY use the information from the context below
2. DO NOT make up or assume anything
3. If the answer is not clearly present, respond EXACTLY with:
   "I don't know based on the provided information."
4. Keep answers concise and clear
5. Do NOT repeat the question
---------------------
Context:
{context}

Question:
{query}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.2
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "I don't know" in response:
        return "Sorry, I couldn't find relevant information. Please contact support."

    return response