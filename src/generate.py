import requests
from retrieve import retrieve
import os

OLLAMA_URL = os.getenv("OLLAMA_URL","http://localhost:11434")

def generate_answer(question,results):
    context = ""
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        context += f"\n[Source: {meta['drug']} - {meta['section']}]\n{doc}\n"

    prompt = f"""You are a medical information assistant helping healthcare professionals look up drug information from official FDA labels.
    Answer the question using ONLY the information provided in the context below.
    If the answer cannot be found in the context, say exactly: "This information is not available in the provided drug labels."
    Do not use any outside knowledge.

    Context:
    {context}

    Question: {question}

    Answer:"""
    response = requests.post(
        f'{OLLAMA_URL}/api/generate',
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()['response']