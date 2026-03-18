from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = None
tokenizer = None

def load_model():
    global model, tokenizer

    if model is None:
        print("Loading model...")

        model_name = "Qwen/Qwen2.5-3B-Instruct"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,  
            device_map="cpu"           
        )

def generate_answer(context, query):
    load_model()

    if not context.strip():
        return "No relevant information found."

    prompt = f"""
You are a StreamKar FAQ assistant.

Answer ONLY from context.
If not found, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.2
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract clean answer
    if "Answer:" in response:
        response = response.split("Answer:")[-1].strip()

    if "I don't know" in response:
        return "Sorry, I couldn't find relevant information."

    return response